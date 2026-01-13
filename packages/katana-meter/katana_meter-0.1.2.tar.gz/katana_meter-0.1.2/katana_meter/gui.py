# -*- coding: utf-8 -*-
"""
Katana Meter – GUI (Analyzer + Optional Mastering)

Flow:
1) Select file once
2) Analyze (LUFS / Peak / ΔE + warnings)
3) Ask: Do you want mastering?
4) Choose target (YouTube / Spotify / Apple / Broadcast / AI Natural)
5) Save output (keeps original format by default)

MP3/FLAC/AAC/OGG decode/encode require ffmpeg in PATH.

2026 Katana Project
"""

from __future__ import annotations

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from .core import analyze_file, master_file


def _default_out_path(input_path: str, mode: str) -> str:
    base, ext = os.path.splitext(input_path)
    ext = ext if ext else ".wav"
    safe_mode = (mode or "mastered").replace(" ", "_")
    return f"{base}_mastered_{safe_mode}{ext}"


class KatanaGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Katana Meter")
        self.geometry("640x420")
        self.resizable(False, False)
        self.configure(bg="#0b1a2e")

        self.file: str | None = None
        self.last_analysis: dict | None = None

        # ---- Header ----
        tk.Label(
            self,
            text="Katana Meter",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#0b1a2e",
        ).pack(pady=12)

        # ---- Buttons ----
        btns = tk.Frame(self, bg="#0b1a2e")
        btns.pack(pady=6)

        tk.Button(btns, text="Dosya Seç", width=14, command=self.pick).grid(row=0, column=0, padx=8)
        tk.Button(btns, text="Analiz Et", width=14, command=self.run_analyze).grid(row=0, column=1, padx=8)
        tk.Button(btns, text="Mastering", width=14, command=self.run_mastering).grid(row=0, column=2, padx=8)

        # ---- Status ----
        self.status = tk.Label(self, text="Bekleniyor", fg="#c8d6ea", bg="#0b1a2e")
        self.status.pack(pady=6)

        # ---- Output ----
        self.out = tk.Text(self, width=74, height=14, bg="#081428", fg="white", font=("Consolas", 11))
        self.out.pack(pady=10)
        self.out.insert("end", "Dosya seç → Analiz Et\n")
        self.out.configure(state="disabled")

    # --------------------------------------------------

    def _set_text(self, text: str) -> None:
        self.out.configure(state="normal")
        self.out.delete("1.0", "end")
        self.out.insert("end", text)
        self.out.configure(state="disabled")

    def _append(self, text: str) -> None:
        self.out.configure(state="normal")
        self.out.insert("end", text)
        self.out.configure(state="disabled")

    def pick(self) -> None:
        path = filedialog.askopenfilename(
            title="Ses Dosyası Seç",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.aac *.ogg"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.file = path
            self.last_analysis = None
            self.status.config(text=path)
            self._set_text(f"Seçildi:\n{path}\n\nAnaliz Et'e bas.\n")

    def run_analyze(self) -> None:
        if not self.file:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")
            return
        self.status.config(text="Analiz ediliyor...")
        threading.Thread(target=self._worker_analyze, daemon=True).start()

    def _worker_analyze(self) -> None:
        try:
            r = analyze_file(self.file)
            self.last_analysis = r
            self.after(0, lambda: self._show_analysis(r))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Hata", str(e)))
            self.after(0, lambda: self.status.config(text="Hata"))

    def _show_analysis(self, r: dict) -> None:
        warns = r.get("warnings") or []
        labels = r.get("labels") or {}
        info = r.get("info") or {}

        text = []
        text.append("ANALYSIS\n")
        text.append(f"File : {self.file}\n")
        text.append(f"Format/Decoder : {info.get('src_format')} / {info.get('decoder')}\n")
        text.append("\n")
        text.append(f"Integrated LUFS : {r['lufs']}\n")
        text.append(f"Gain to target  : {r['gain_to_target_db']} dB (target {r['target_lufs']})\n")
        text.append(f"Peak (approx)   : {r['peak_dbtp_approx']} dB\n")
        text.append(f"ΔE              : {r['delta_e']}\n")
        text.append("\n")
        text.append("Labels:\n")
        text.append(f"  loudness   : {labels.get('loudness')}\n")
        text.append(f"  peak_risk  : {labels.get('peak_risk')}\n")
        text.append(f"  action     : {labels.get('gain_action')}\n")

        if warns:
            text.append("\nWarnings:\n")
            for w in warns:
                text.append(f"  - {w}\n")
        else:
            text.append("\nWarnings: none\n")

        text.append("\nİstersen şimdi 'Mastering' butonuna bas.\n")

        self._set_text("".join(text))
        self.status.config(text="Analiz tamam ✓")

    # --------------------------------------------------
    # Mastering
    # --------------------------------------------------

    def run_mastering(self) -> None:
        if not self.file:
            messagebox.showwarning("Uyarı", "Önce dosya seç.")
            return

        # Eğer analiz yapılmadıysa otomatik yap
        if not self.last_analysis:
            if not messagebox.askyesno("Mastering", "Önce analiz yapılmamış. Analiz edip devam edelim mi?"):
                return
            self.run_analyze()
            return

        if not messagebox.askyesno("Mastering", "Bu ölçümlerle mastering yapmak ister misin?"):
            return

        mode = self._ask_mode()
        if not mode:
            return

        # aynı formatı koruyacak şekilde default çıktı adı
        suggested = _default_out_path(self.file, mode)
        out_path = filedialog.asksaveasfilename(
            title="Mastered dosyayı kaydet",
            initialfile=os.path.basename(suggested),
            initialdir=os.path.dirname(self.file),
            defaultextension=os.path.splitext(suggested)[1],
            filetypes=[
                ("Same as input", f"*{os.path.splitext(self.file)[1]}"),
                ("WAV", "*.wav"),
                ("MP3", "*.mp3"),
                ("FLAC", "*.flac"),
                ("AAC", "*.aac"),
                ("OGG", "*.ogg"),
                ("All files", "*.*"),
            ],
        )
        if not out_path:
            return

        self.status.config(text=f"Mastering ({mode})...")
        threading.Thread(target=self._worker_master, args=(mode, out_path), daemon=True).start()

    def _ask_mode(self) -> str | None:
        win = tk.Toplevel(self)
        win.title("Mastering Target")
        win.geometry("360x260")
        win.resizable(False, False)
        win.configure(bg="#0b1a2e")
        win.grab_set()

        tk.Label(win, text="Hedef seç:", fg="white", bg="#0b1a2e", font=("Arial", 12, "bold")).pack(pady=12)

        var = tk.StringVar(value="youtube")

        options = [
            ("YouTube (-14 LUFS / -1 dB)", "youtube"),
            ("Spotify (-14 LUFS / -1 dB)", "spotify"),
            ("Apple Music (-16 LUFS / -1 dB)", "apple"),
            ("Broadcast (-23 LUFS / -1 dB)", "broadcast"),
            ("AI Natural (ΔE-aware)", "ai_natural"),
        ]

        box = tk.Frame(win, bg="#0b1a2e")
        box.pack(pady=6)

        for text, val in options:
            tk.Radiobutton(
                box, text=text, value=val, variable=var,
                fg="white", bg="#0b1a2e", selectcolor="#081428",
                activebackground="#0b1a2e", activeforeground="white",
                anchor="w", width=32
            ).pack(pady=3, padx=10)

        out: dict[str, str | None] = {"mode": None}

        def ok():
            out["mode"] = var.get()
            win.destroy()

        def cancel():
            out["mode"] = None
            win.destroy()

        btns = tk.Frame(win, bg="#0b1a2e")
        btns.pack(pady=14)
        tk.Button(btns, text="OK", width=10, command=ok).grid(row=0, column=0, padx=8)
        tk.Button(btns, text="İptal", width=10, command=cancel).grid(row=0, column=1, padx=8)

        self.wait_window(win)
        return out["mode"]  # type: ignore[return-value]

    def _worker_master(self, mode: str, out_path: str) -> None:
        try:
            res = master_file(self.file, out_path, mode=mode)
            self.after(0, lambda: self._show_master_result(res))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Hata", str(e)))
            self.after(0, lambda: self.status.config(text="Hata"))

    def _show_master_result(self, res: dict) -> None:
        self.status.config(text="Mastering tamam ✓")

        pre = res.get("pre") or {}
        post = res.get("post") or {}
        enc = res.get("encode") or {}
        dec = res.get("decode") or {}

        self._append("\n\nMASTERING RESULT\n")
        self._append(f"Mode   : {res.get('mode')}\n")
        self._append(f"Output : {res.get('output_path')}\n")
        self._append(f"Decode : {dec.get('decoder')} ({dec.get('src_format')})\n")
        self._append(f"Encode : {enc.get('encoder')} ({enc.get('format')})\n")
        self._append("\nBefore:\n")
        self._append(f"  LUFS : {pre.get('lufs')}\n")
        self._append(f"  Peak : {pre.get('peak_dbtp_approx')}\n")
        self._append(f"  ΔE   : {pre.get('delta_e')}\n")
        self._append("\nAfter:\n")
        self._append(f"  LUFS : {post.get('lufs')}\n")
        self._append(f"  Peak : {post.get('peak_dbtp_approx')}\n")
        self._append(f"  ΔE   : {post.get('delta_e')}\n")


def main() -> None:
    KatanaGUI().mainloop()


if __name__ == "__main__":
    main()
