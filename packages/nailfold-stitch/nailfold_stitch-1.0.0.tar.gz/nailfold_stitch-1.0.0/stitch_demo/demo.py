import os
import glob
import threading
import queue
import argparse
from typing import List, Optional

import cv2
import numpy as np
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# =============================
#（SURF+满二叉树+特征点上限）
# =============================
def enhance_bgr(img: np.ndarray) -> np.ndarray:
    b, g, r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def _one_channel(ch: np.ndarray) -> np.ndarray:
        ch = clahe.apply(ch)
        ch = cv2.bilateralFilter(ch, 20, 10, 10)
        blur = cv2.GaussianBlur(ch, (0, 0), 80)
        ch = cv2.addWeighted(ch, 1.5, blur, -0.5, 0)
        return ch

    return cv2.merge([_one_channel(b), _one_channel(g), _one_channel(r)])


# URF特征检测器，调节特征点上限（用于拼接匹配不成功时手动调节参数实现全景拼接）
def create_feature_detector(max_keypoints: int = 600):
    """创建SURF检测器，通过hessianThreshold+响应值排序实现特征点上限控制"""
    if not hasattr(cv2, "xfeatures2d") or not hasattr(cv2.xfeatures2d, "SURF_create"):
        raise RuntimeError("SURF 不可用：请安装 opencv-contrib-python 版本（3.4.2.16）")

    # SURF参数：hessianThreshold设为较小值（确保检测足够多的特征点），后续按上限截取
    # max_keypoints越大，hessianThreshold越小（检测更多特征点）
    hessian_threshold = max(10, 500 - (max_keypoints // 5))  # 动态调整阈值
    surf = cv2.xfeatures2d.SURF_create(hessianThreshold=hessian_threshold)
    return "surf", surf, "flann_float", max_keypoints


def match_descriptors(des1, des2, matcher_type: str, ratio: float = 0.75):
    if des1 is None or des2 is None:
        return []

    if matcher_type == "flann_float":
        index_params = dict(algorithm=1, trees=5)  # KDTree
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
    else:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m_n in matches:
        if len(m_n) != 2:
            continue
        m, n = m_n
        if m.distance < ratio * n.distance:
            good.append(m)
    return good


def crop_to_content(img: np.ndarray, pad: int = 2) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = gray > 0
    if not np.any(mask):
        return img
    ys, xs = np.where(mask)
    y0, y1 = ys.min(), ys.max()
    x0, x1 = xs.min(), xs.max()
    y0 = max(0, y0 - pad)
    x0 = max(0, x0 - pad)
    y1 = min(img.shape[0] - 1, y1 + pad)
    x1 = min(img.shape[1] - 1, x1 + pad)
    return img[y0 : y1 + 1, x0 : x1 + 1]


def stitch_pair(
    left_path: str,
    right_path: str,
    out_path: str,
    preprocess: bool = True,
    min_matches: int = 12,
    max_keypoints: int = 600
) -> str:
    right_img = cv2.imread(right_path)
    left_img = cv2.imread(left_path)

    if right_img is None:
        raise FileNotFoundError(f"无法读取：{right_path}")
    if left_img is None:
        raise FileNotFoundError(f"无法读取：{left_path}")

    if preprocess:
        right_img = enhance_bgr(right_img)
        left_img = enhance_bgr(left_img)

    # 使用SURF检测器
    det_name, detector, matcher_type, max_kp = create_feature_detector(max_keypoints)
    kp1, des1 = detector.detectAndCompute(right_img, None)
    kp2, des2 = detector.detectAndCompute(left_img, None)

    # 截取前max_keypoints个特征点（确保不超过上限）
    def limit_keypoints(kp, des, max_kp):
        if len(kp) <= max_kp:
            return kp, des
    # 按响应值（response）降序排序（响应值越高，特征点质量越好）
        sorted_indices = sorted(range(len(kp)), key=lambda i: kp[i].response, reverse=True)
        limited_kp = [kp[i] for i in sorted_indices[:max_kp]]
        limited_des = des[sorted_indices[:max_kp]] if des is not None else None
        return limited_kp, limited_des

    kp1, des1 = limit_keypoints(kp1, des1, max_kp)
    kp2, des2 = limit_keypoints(kp2, des2, max_kp)

    # 验证特征点数量
    if len(kp1) == 0 or len(kp2) == 0:
        raise RuntimeError(f"特征点检测失败：右图={len(kp1)}个，左图={len(kp2)}个")

    # 匹配特征点
    good = match_descriptors(des1, des2, matcher_type, ratio=0.75)
    if len(good) < min_matches:
        raise RuntimeError(f"匹配点不足：{len(good)}/{min_matches}（方法：{det_name}，特征点上限={max_kp}）")

    # 计算单应性矩阵
    pts_right = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts_left = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    H, _ = cv2.findHomography(pts_right, pts_left, cv2.RANSAC, 5.0)
    if H is None:
        raise RuntimeError("findHomography 失败（可能重叠不足/特征太少/图像模糊）")

    # 图像拼接
    hR, wR = right_img.shape[:2]
    hL, wL = left_img.shape[:2]

    right_border = np.float32([[[0, 0], [wR, 0], [wR, hR], [0, hR]]])
    right_border_in_left = cv2.perspectiveTransform(right_border, H)

    max_x = int(max(wL, np.max(right_border_in_left[:, :, 0])))
    max_y = int(max(hL, np.max(right_border_in_left[:, :, 1])))
    max_x = max(max_x, wL)
    max_y = max(max_y, hL)

    warped_right = cv2.warpPerspective(right_img, H, (max_x, max_y))

    dst = warped_right.copy()
    dst[0:hL, 0:wL] = left_img

    # 重叠区域融合
    start = float(min(right_border_in_left[0][0][0], right_border_in_left[0][3][0]))
    start = int(max(0, min(start, wL - 1)))

    overlap_width = max(1, wL - start)
    ramp = (np.arange(start, wL, dtype=np.float32) - start) / float(overlap_width)
    ramp = ramp.reshape(1, -1, 1)

    for y in range(min(dst.shape[0], warped_right.shape[0])):
        left_row = dst[y, start:wL].astype(np.float32)
        right_row = warped_right[y, start:wL].astype(np.float32)

        right_mask = (right_row.sum(axis=1, keepdims=True) > 0).astype(np.float32)
        alpha = ramp[0] * right_mask

        blended = left_row * (1.0 - alpha) + right_row * alpha
        dst[y, start:wL] = np.clip(blended, 0, 255).astype(np.uint8)

    dst = crop_to_content(dst)
    cv2.imwrite(out_path, dst)
    return out_path


def list_images(input_dir: str) -> List[str]:
    exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff")
    paths = []
    for e in exts:
        paths.extend(glob.glob(os.path.join(input_dir, e)))
    return sorted(paths)


# 满二叉树两两拼接逻辑（添加特征点上限参数）
def run_tree_stitch(
    image_paths: List[str],
    work_dir: str,
    output_path: str,
    preprocess: bool,
    log_fn,
    max_keypoints: int = 600
):
    os.makedirs(work_dir, exist_ok=True)

    if len(image_paths) == 0:
        raise ValueError("未找到任何图片")
    if len(image_paths) == 1:
        img = cv2.imread(image_paths[0])
        if img is None:
            raise FileNotFoundError(image_paths[0])
        cv2.imwrite(output_path, img)
        return output_path

    current_paths = image_paths.copy()
    round_num = 1
    total_counter = 0

    log_fn(f"===== 满二叉树拼接开始（SURF+特征点上限={max_keypoints}）=====")
    log_fn(f"初始图片数量：{len(current_paths)}")

    while len(current_paths) > 1:
        next_paths = []
        log_fn(f"\n===== 第 {round_num} 轮拼接 =====")

        for i in range(0, len(current_paths), 2):
            if i + 1 >= len(current_paths):
                log_fn(f"⚠️ 第 {round_num} 轮剩余单张图片：{os.path.basename(current_paths[i])}，直接进入下一轮")
                next_paths.append(current_paths[i])
                continue

            total_counter += 1
            left_path = current_paths[i]
            right_path = current_paths[i + 1]
            out_path = os.path.join(work_dir, f"round{round_num}_group{i//2 + 1:02d}.jpg")

            log_fn(f"[{round_num}轮-{i//2 + 1}组] 拼接：LEFT={os.path.basename(left_path)} + RIGHT={os.path.basename(right_path)}")
            log_fn(f"[{round_num}轮-{i//2 + 1}组] 特征点上限：{max_keypoints}")
            try:
                stitched = stitch_pair(
                    left_path=left_path,
                    right_path=right_path,
                    out_path=out_path,
                    preprocess=preprocess,
                    max_keypoints=max_keypoints
                )
                next_paths.append(stitched)
                log_fn(f"✅ [{round_num}轮-{i//2 + 1}组] 拼接完成：{os.path.basename(stitched)}")
            except Exception as e:
                log_fn(f"❌ [{round_num}轮-{i//2 + 1}组] 拼接失败：{e}")
                raise

        current_paths = next_paths
        log_fn(f"===== 第 {round_num} 轮拼接结束，剩余图片数量：{len(current_paths)} =====")
        round_num += 1

    final_img = cv2.imread(current_paths[0])
    if final_img is None:
        raise RuntimeError("最终结果读取失败")
    cv2.imwrite(output_path, final_img)
    log_fn(f"\n✅ 满二叉树拼接完成，最终结果保存至：{output_path}")
    return output_path

# =============================
# GUI（SURF+满二叉树+特征点上限调节）
# =============================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("甲襞毛细血管图像全景拼接 Demo")
        self.geometry("980x650")

        self.log_q = queue.Queue()
        self.worker = None
        self.preview_imgtk = None

        # 保留特征点上限变量（默认600）
        self.var_input_dir = tk.StringVar(value="")
        self.var_output = tk.StringVar(value=os.path.abspath("result.jpg"))
        self.var_work_dir = tk.StringVar(value=os.path.abspath("_stitch_work"))
        self.var_preprocess = tk.BooleanVar(value=True)
        self.var_max_keypoints = tk.IntVar(value=600)  # 特征点上限变量

        self._build_ui()
        self.after(100, self._poll_log_queue)

    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # 路径选择
        row1 = ttk.Frame(frm)
        row1.pack(fill="x", pady=4)
        ttk.Label(row1, text="输入图片文件：").pack(side="left")
        ttk.Entry(row1, textvariable=self.var_input_dir, width=60).pack(side="left", padx=6)
        ttk.Button(row1, text="选择...", command=self.pick_input_dir).pack(side="left")

        row2 = ttk.Frame(frm)
        row2.pack(fill="x", pady=4)
        ttk.Label(row2, text="输出图片文件：").pack(side="left")
        ttk.Entry(row2, textvariable=self.var_output, width=60).pack(side="left", padx=6)
        ttk.Button(row2, text="选择...", command=self.pick_output_file).pack(side="left")

        row3 = ttk.Frame(frm)
        row3.pack(fill="x", pady=4)
        ttk.Label(row3, text="中间结果目录：").pack(side="left")
        ttk.Entry(row3, textvariable=self.var_work_dir, width=60).pack(side="left", padx=6)
        ttk.Button(row3, text="选择...", command=self.pick_work_dir).pack(side="left")

        row4 = ttk.Frame(frm)
        row4.pack(fill="x", pady=6)

        ttk.Label(row4, text="特征点上限：").pack(side="left")
        max_kp_spin = ttk.Spinbox(
            row4,
            textvariable=self.var_max_keypoints,
            from_=100,
            to=5000,
            increment=100,
            width=10,
            state="readonly"
        )
        max_kp_spin.pack(side="left", padx=6)

        # 预处理开关
        ttk.Checkbutton(row4, text="启用预处理增强", variable=self.var_preprocess).pack(side="left", padx=12)

        # 拼接按钮
        self.btn_run = ttk.Button(row4, text="开始拼接", command=self.start)
        self.btn_run.pack(side="right")

        # 进度条
        self.pb = ttk.Progressbar(frm, mode="indeterminate")
        self.pb.pack(fill="x", pady=6)

        # 日志+预览区域
        split = ttk.Panedwindow(frm, orient="horizontal")
        split.pack(fill="both", expand=True, pady=8)
        left = ttk.Frame(split)
        right = ttk.Frame(split)
        split.add(left, weight=2)
        split.add(right, weight=3)

        # 日志区域
        ttk.Label(left, text="运行日志：").pack(anchor="w")
        self.txt = tk.Text(left, height=20, wrap="word")
        self.txt.pack(fill="both", expand=True)
        self.txt.configure(state="disabled")

        # 预览区域
        ttk.Label(right, text="结果预览：").pack(anchor="w")
        self.preview = ttk.Label(right, text="完成后会在这里显示结果图")
        self.preview.pack(fill="both", expand=True, pady=8)

        # 底部按钮
        bottom = ttk.Frame(frm)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="清空日志", command=self.clear_log).pack(side="left")
        ttk.Button(bottom, text="打开输出文件夹", command=self.open_output_dir).pack(side="left", padx=8)

    def log(self, s: str):
        self.log_q.put(s)

    def _poll_log_queue(self):
        try:
            while True:
                s = self.log_q.get_nowait()
                self.txt.configure(state="normal")
                self.txt.insert("end", s + "\n")
                self.txt.see("end")
                self.txt.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self._poll_log_queue)

    def clear_log(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.configure(state="disabled")

    def pick_input_dir(self):
        d = filedialog.askdirectory(title="选择输入图片文件夹")
        if d:
            self.var_input_dir.set(d)

    def pick_work_dir(self):
        d = filedialog.askdirectory(title="选择中间结果输出目录")
        if d:
            self.var_work_dir.set(d)

    def pick_output_file(self):
        f = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All files", "*.*")],
        )
        if f:
            self.var_output.set(f)

    def open_output_dir(self):
        out = self.var_output.get().strip()
        if not out:
            return
        folder = os.path.dirname(os.path.abspath(out))
        if os.path.isdir(folder):
            try:
                if os.name == "nt":
                    os.startfile(folder)
                elif os.name == "posix":
                    import subprocess
                    subprocess.Popen(["xdg-open", folder])
            except Exception as e:
                messagebox.showerror("错误", f"打开文件夹失败：{e}")

    def start(self):
        if self.worker and self.worker.is_alive():
            messagebox.showinfo("提示", "正在运行中，请稍等…")
            return

        input_dir = self.var_input_dir.get().strip()
        output_path = self.var_output.get().strip()
        work_dir = self.var_work_dir.get().strip()
        preprocess = bool(self.var_preprocess.get())
        max_keypoints = self.var_max_keypoints.get()  # 获取用户设置的特征点上限

        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("错误", "请输入/选择有效的输入图片文件夹")
            return
        if not output_path:
            messagebox.showerror("错误", "请选择输出文件路径")
            return

        self.btn_run.configure(state="disabled")
        self.pb.start(10)
        self.preview.configure(image="", text="正在满二叉树拼接（SURF）…")
        self.preview_imgtk = None

        def _run():
            try:
                paths = list_images(input_dir)
                self.log(f"📁 找到 {len(paths)} 张图片（按文件名排序）：")
                for idx, p in enumerate(paths, 1):
                    self.log(f"   {idx}. {os.path.basename(p)}")
                # 打印当前设置（包含特征点上限）
                self.log(f"\n⚙️ 当前设置：特征方法=SURF，特征点上限={max_keypoints}，预处理={preprocess}")

                out = run_tree_stitch(
                    image_paths=paths,
                    work_dir=work_dir,
                    output_path=output_path,
                    preprocess=preprocess,
                    log_fn=self.log,
                    max_keypoints=max_keypoints  # 传递特征点上限参数
                )
                self._show_preview(out)
            except Exception as e:
                self.log(f"\n❌ 拼接失败：{repr(e)}")
                messagebox.showerror("运行失败", str(e))
            finally:
                self.pb.stop()
                self.btn_run.configure(state="normal")

        self.worker = threading.Thread(target=_run, daemon=True)
        self.worker.start()

    def _show_preview(self, img_path: str):
        try:
            img = Image.open(img_path).convert("RGB")
            max_w, max_h = 620, 520
            w, h = img.size
            scale = min(max_w / w, max_h / h, 1.0)
            img = img.resize((int(w * scale), int(h * scale)))
            self.preview_imgtk = ImageTk.PhotoImage(img)
            self.preview.configure(image=self.preview_imgtk, text="")
        except Exception as e:
            self.log(f"预览失败：{e}")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()