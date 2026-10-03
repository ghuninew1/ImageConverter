import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageOps

# Required for AVIF support
try:
    import pillow_avif  # noqa: F401
except ImportError:
    pass


SUPPORTED_FORMATS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".avif",
}


class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.root.geometry("700x560")
        self.root.minsize(650, 500)

        self.folder = tk.StringVar()

        self.width = tk.StringVar(value="800")
        self.height = tk.StringVar(value="")

        self.webp_quality = tk.IntVar(value=85)
        self.avif_quality = tk.IntVar(value=50)

        self.create_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def create_ui(self):
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main,
            text="Image Converter",
            font=("TkDefaultFont", 20, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Convert images to WebP / AVIF or resize images",
        ).pack(anchor="w", pady=(0, 20))

        # Folder
        folder_frame = ttk.LabelFrame(
            main,
            text="Input Folder",
            padding=10,
        )
        folder_frame.pack(fill="x", pady=(0, 15))

        ttk.Entry(
            folder_frame,
            textvariable=self.folder,
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            folder_frame,
            text="Browse...",
            command=self.select_folder,
        ).pack(side="left", padx=(10, 0))

        # Conversion
        convert_frame = ttk.LabelFrame(
            main,
            text="Convert",
            padding=10,
        )
        convert_frame.pack(fill="x", pady=(0, 15))

        ttk.Button(
            convert_frame,
            text="Convert to WebP",
            command=self.start_webp,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            convert_frame,
            text="Convert to AVIF",
            command=self.start_avif,
        ).pack(side="left")

        # Quality
        quality_frame = ttk.Frame(convert_frame)
        quality_frame.pack(side="right")

        ttk.Label(
            quality_frame,
            text="WebP Quality:",
        ).pack(side="left")

        ttk.Spinbox(
            quality_frame,
            from_=1,
            to=100,
            width=5,
            textvariable=self.webp_quality,
        ).pack(side="left", padx=(5, 15))

        ttk.Label(
            quality_frame,
            text="AVIF Quality:",
        ).pack(side="left")

        ttk.Spinbox(
            quality_frame,
            from_=1,
            to=100,
            width=5,
            textvariable=self.avif_quality,
        ).pack(side="left", padx=5)

        # Resize
        resize_frame = ttk.LabelFrame(
            main,
            text="Resize",
            padding=10,
        )
        resize_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            resize_frame,
            text="Width:",
        ).pack(side="left")

        ttk.Entry(
            resize_frame,
            textvariable=self.width,
            width=8,
        ).pack(side="left", padx=(5, 15))

        ttk.Label(
            resize_frame,
            text="Height:",
        ).pack(side="left")

        ttk.Entry(
            resize_frame,
            textvariable=self.height,
            width=8,
        ).pack(side="left", padx=5)

        ttk.Label(
            resize_frame,
            text="(leave empty = square)",
        ).pack(side="left", padx=(10, 20))

        ttk.Button(
            resize_frame,
            text="Resize",
            command=self.start_resize,
        ).pack(side="right")

        # Progress
        self.progress = ttk.Progressbar(
            main,
            mode="determinate",
        )
        self.progress.pack(fill="x", pady=(5, 10))

        # Log
        log_frame = ttk.LabelFrame(
            main,
            text="Log",
            padding=10,
        )
        log_frame.pack(fill="both", expand=True)

        self.log = tk.Text(
            log_frame,
            height=12,
            wrap="word",
            state="disabled",
        )
        self.log.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar = ttk.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.log.yview,
        )
        scrollbar.pack(side="right", fill="y")

        self.log.configure(
            yscrollcommand=scrollbar.set
        )

        # Bottom
        ttk.Button(
            main,
            text="Clear Log",
            command=self.clear_log,
        ).pack(anchor="e", pady=(10, 0))

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def select_folder(self):
        folder = filedialog.askdirectory(
            title="Select Image Folder"
        )

        if folder:
            self.folder.set(folder)
            self.write_log(f"Selected folder: {folder}")

    def get_files(self):
        folder = Path(self.folder.get())

        if not folder.exists():
            messagebox.showerror(
                "Error",
                "Please select a valid folder.",
            )
            return []

        return [
            file
            for file in folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_FORMATS
        ]

    def open_image(self, file):
        image = Image.open(file)

        # Fix EXIF orientation
        image = ImageOps.exif_transpose(image)

        return image

    def write_log(self, message):
        self.root.after(
            0,
            lambda: self._write_log(message),
        )

    def _write_log(self, message):
        self.log.configure(state="normal")

        self.log.insert(
            "end",
            message + "\n",
        )

        self.log.see("end")
        self.log.configure(state="disabled")

    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def start_progress(self, total):
        self.root.after(
            0,
            lambda: self._start_progress(total),
        )

    def _start_progress(self, total):
        self.progress["maximum"] = total
        self.progress["value"] = 0

    def update_progress(self):
        self.root.after(
            0,
            lambda: self.progress.step(1),
        )

    def finish(self, message):
        self.root.after(
            0,
            lambda: messagebox.showinfo(
                "Finished",
                message,
            ),
        )

    # ---------------------------------------------------------
    # WebP
    # ---------------------------------------------------------

    def start_webp(self):
        files = self.get_files()

        if not files:
            return

        threading.Thread(
            target=self.convert_webp,
            args=(files,),
            daemon=True,
        ).start()

    def convert_webp(self, files):
        self.start_progress(len(files))

        converted = 0

        for file in files:

            if file.suffix.lower() == ".webp":
                self.write_log(
                    f"Skipping: {file.name}"
                )
                self.update_progress()
                continue

            output = file.with_suffix(".webp")

            try:
                image = self.open_image(file)

                if image.mode not in ("RGB", "RGBA"):
                    if "A" in image.getbands():
                        image = image.convert("RGBA")
                    else:
                        image = image.convert("RGB")

                image.save(
                    output,
                    "WEBP",
                    quality=self.webp_quality.get(),
                    method=6,
                )

                converted += 1

                self.write_log(
                    f"✓ {file.name} → {output.name}"
                )

            except Exception as error:
                self.write_log(
                    f"✗ {file.name}: {error}"
                )

            self.update_progress()

        self.finish(
            f"WebP conversion finished.\n\n"
            f"Converted: {converted}"
        )

    # ---------------------------------------------------------
    # AVIF
    # ---------------------------------------------------------

    def start_avif(self):
        files = self.get_files()

        if not files:
            return

        threading.Thread(
            target=self.convert_avif,
            args=(files,),
            daemon=True,
        ).start()

    def convert_avif(self, files):
        self.start_progress(len(files))

        converted = 0

        for file in files:

            if file.suffix.lower() == ".avif":
                self.write_log(
                    f"Skipping: {file.name}"
                )
                self.update_progress()
                continue

            output = file.with_suffix(".avif")

            try:
                image = self.open_image(file)

                if image.mode not in ("RGB", "RGBA"):
                    if "A" in image.getbands():
                        image = image.convert("RGBA")
                    else:
                        image = image.convert("RGB")

                image.save(
                    output,
                    "AVIF",
                    quality=self.avif_quality.get(),
                )

                converted += 1

                self.write_log(
                    f"✓ {file.name} → {output.name}"
                )

            except Exception as error:
                self.write_log(
                    f"✗ {file.name}: {error}"
                )

            self.update_progress()

        self.finish(
            f"AVIF conversion finished.\n\n"
            f"Converted: {converted}"
        )

    # ---------------------------------------------------------
    # Resize
    # ---------------------------------------------------------

    def start_resize(self):
        files = self.get_files()

        if not files:
            return

        try:
            width = int(self.width.get())

            if width <= 0:
                raise ValueError

            if self.height.get().strip():
                height = int(self.height.get())

                if height <= 0:
                    raise ValueError
            else:
                height = width

        except ValueError:
            messagebox.showerror(
                "Error",
                "Width and Height must be valid numbers.",
            )
            return

        threading.Thread(
            target=self.resize_files,
            args=(files, width, height),
            daemon=True,
        ).start()

    def resize_files(self, files, width, height):
        self.start_progress(len(files))

        resized = 0

        for file in files:

            output = file.with_name(
                f"{file.stem}-{width}x{height}"
                f"{file.suffix}"
            )

            try:
                image = self.open_image(file)

                image = image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS,
                )

                image.save(output)

                resized += 1

                self.write_log(
                    f"✓ {file.name} → {output.name}"
                )

            except Exception as error:
                self.write_log(
                    f"✗ {file.name}: {error}"
                )

            self.update_progress()

        self.finish(
            f"Resize finished.\n\n"
            f"Resized: {resized}"
        )


# -------------------------------------------------------------
# Start Application
# -------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()

    app = ImageConverterApp(root)

    root.mainloop()