from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageOps
from tkinterdnd2 import DND_FILES, TkinterDnD


# ============================================================
# Supported formats
# ============================================================

SUPPORTED_INPUT_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
    ".ico",
}

OUTPUT_FORMATS = {
    "WebP": ".webp",
    "AVIF": ".avif",
    "JPEG": ".jpg",
    "PNG": ".png",
    "BMP": ".bmp",
    "TIFF": ".tiff",
    "GIF": ".gif",
    "ICO": ".ico",
}


class ImageConverterApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Image Converter")
        self.root.geometry("850x700")
        self.root.minsize(750, 600)

        self.files = []

        # Conversion settings
        self.output_format = tk.StringVar(value="WebP")
        self.quality = tk.IntVar(value=85)

        self.width = tk.StringVar(value="")
        self.height = tk.StringVar(value="")

        self.keep_aspect = tk.BooleanVar(value=True)

        # Progress
        self.total_files = 0
        self.completed_files = 0
        self.converted_files = 0
        self.skipped_files = 0
        self.failed_files = 0

        self.current_file = tk.StringVar(value="Waiting...")

        self.create_ui()

    # ========================================================
    # UI
    # ========================================================

    def create_ui(self):

        main = ttk.Frame(
            self.root,
            padding=15,
        )

        main.pack(
            fill="both",
            expand=True,
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        ttk.Label(
            main,
            text="Image Converter",
            font=("TkDefaultFont", 22, "bold"),
        ).pack(
            anchor="w",
        )

        ttk.Label(
            main,
            text="Convert and resize images",
        ).pack(
            anchor="w",
            pady=(0, 12),
        )

        # ----------------------------------------------------
        # Notebook
        # ----------------------------------------------------

        self.notebook = ttk.Notebook(main)

        self.notebook.pack(
            fill="both",
            expand=True,
        )

        self.converter_tab = ttk.Frame(
            self.notebook,
            padding=15,
        )

        self.progress_tab = ttk.Frame(
            self.notebook,
            padding=15,
        )

        self.notebook.add(
            self.converter_tab,
            text="Converter",
        )

        self.notebook.add(
            self.progress_tab,
            text="Progress",
        )

        self.create_converter_tab()
        self.create_progress_tab()

    # ========================================================
    # Converter Tab
    # ========================================================

    def create_converter_tab(self):

        parent = self.converter_tab

        # ----------------------------------------------------
        # Drag & Drop
        # ----------------------------------------------------

        self.drop_area = tk.Label(
            parent,
            text=(
                "DROP FILES OR FOLDERS HERE\n\n"
                "or click to select files"
            ),
            relief="groove",
            borderwidth=2,
            height=6,
            font=("TkDefaultFont", 13),
        )

        self.drop_area.pack(
            fill="x",
            pady=(0, 12),
        )

        self.drop_area.drop_target_register(
            DND_FILES
        )

        self.drop_area.dnd_bind(
            "<<Drop>>",
            self.handle_drop,
        )

        self.drop_area.bind(
            "<Button-1>",
            self.select_files,
        )

        # ----------------------------------------------------
        # File list
        # ----------------------------------------------------

        list_frame = ttk.LabelFrame(
            parent,
            text="Files",
            padding=8,
        )

        list_frame.pack(
            fill="both",
            expand=False,
            pady=(0, 10),
        )

        self.file_list = tk.Listbox(
            list_frame,
            height=6,
        )

        self.file_list.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.file_list.yview,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.file_list.configure(
            yscrollcommand=scrollbar.set
        )

        # ----------------------------------------------------
        # File buttons
        # ----------------------------------------------------

        file_buttons = ttk.Frame(parent)

        file_buttons.pack(
            fill="x",
            pady=(0, 12),
        )

        ttk.Button(
            file_buttons,
            text="Add Files",
            command=self.select_files,
        ).pack(
            side="left",
            padx=(0, 5),
        )

        ttk.Button(
            file_buttons,
            text="Add Folder",
            command=self.select_folder,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            file_buttons,
            text="Clear",
            command=self.clear_files,
        ).pack(
            side="left",
            padx=5,
        )

        # ----------------------------------------------------
        # Convert settings
        # ----------------------------------------------------

        convert_frame = ttk.LabelFrame(
            parent,
            text="Convert",
            padding=10,
        )

        convert_frame.pack(
            fill="x",
            pady=(0, 10),
        )

        ttk.Label(
            convert_frame,
            text="Output:",
        ).pack(
            side="left",
        )

        self.format_combo = ttk.Combobox(
            convert_frame,
            textvariable=self.output_format,
            values=list(OUTPUT_FORMATS.keys()),
            state="readonly",
            width=10,
        )

        self.format_combo.pack(
            side="left",
            padx=(8, 20),
        )

        ttk.Label(
            convert_frame,
            text="Quality:",
        ).pack(
            side="left",
        )

        ttk.Spinbox(
            convert_frame,
            from_=1,
            to=100,
            textvariable=self.quality,
            width=5,
        ).pack(
            side="left",
            padx=8,
        )

        # ----------------------------------------------------
        # Resize
        # ----------------------------------------------------

        resize_frame = ttk.LabelFrame(
            parent,
            text="Resize",
            padding=10,
        )

        resize_frame.pack(
            fill="x",
            pady=(0, 10),
        )

        ttk.Label(
            resize_frame,
            text="Width:",
        ).pack(
            side="left",
        )

        ttk.Entry(
            resize_frame,
            textvariable=self.width,
            width=8,
        ).pack(
            side="left",
            padx=(5, 15),
        )

        ttk.Label(
            resize_frame,
            text="Height:",
        ).pack(
            side="left",
        )

        ttk.Entry(
            resize_frame,
            textvariable=self.height,
            width=8,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Checkbutton(
            resize_frame,
            text="Keep Aspect Ratio",
            variable=self.keep_aspect,
        ).pack(
            side="left",
            padx=15,
        )

        # ----------------------------------------------------
        # Start
        # ----------------------------------------------------

        self.start_button = ttk.Button(
            parent,
            text="START CONVERSION",
            command=self.start_conversion,
        )

        self.start_button.pack(
            fill="x",
            ipady=8,
            pady=(5, 0),
        )

    # ========================================================
    # Progress Tab
    # ========================================================

    def create_progress_tab(self):

        parent = self.progress_tab

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        status_frame = ttk.LabelFrame(
            parent,
            text="Conversion Status",
            padding=15,
        )

        status_frame.pack(
            fill="x",
            pady=(0, 15),
        )

        self.progress_percent = tk.StringVar(
            value="0%"
        )

        self.progress_count = tk.StringVar(
            value="0 / 0 files"
        )

        ttk.Label(
            status_frame,
            textvariable=self.progress_percent,
            font=("TkDefaultFont", 28, "bold"),
        ).pack()

        ttk.Label(
            status_frame,
            textvariable=self.progress_count,
            font=("TkDefaultFont", 12),
        ).pack(
            pady=(5, 10)
        )

        self.progress = ttk.Progressbar(
            status_frame,
            mode="determinate",
        )

        self.progress.pack(
            fill="x",
        )

        # ----------------------------------------------------
        # Current file
        # ----------------------------------------------------

        current_frame = ttk.LabelFrame(
            parent,
            text="Current File",
            padding=10,
        )

        current_frame.pack(
            fill="x",
            pady=(0, 15),
        )

        ttk.Label(
            current_frame,
            textvariable=self.current_file,
        ).pack(
            anchor="w",
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        stats_frame = ttk.LabelFrame(
            parent,
            text="Statistics",
            padding=10,
        )

        stats_frame.pack(
            fill="x",
            pady=(0, 15),
        )

        self.stats_label = ttk.Label(
            stats_frame,
            text=(
                "Converted: 0    "
                "Skipped: 0    "
                "Failed: 0"
            ),
        )

        self.stats_label.pack(
            anchor="w",
        )

        # ----------------------------------------------------
        # Log
        # ----------------------------------------------------

        log_frame = ttk.LabelFrame(
            parent,
            text="Log",
            padding=10,
        )

        log_frame.pack(
            fill="both",
            expand=True,
        )

        self.log = tk.Text(
            log_frame,
            wrap="word",
            state="disabled",
        )

        self.log.pack(
            side="left",
            fill="both",
            expand=True,
        )

        log_scroll = ttk.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.log.yview,
        )

        log_scroll.pack(
            side="right",
            fill="y",
        )

        self.log.configure(
            yscrollcommand=log_scroll.set,
        )

    # ========================================================
    # Drag & Drop
    # ========================================================

    def handle_drop(self, event):

        paths = self.root.tk.splitlist(
            event.data
        )

        self.add_paths(paths)

    # ========================================================
    # Select files
    # ========================================================

    def select_files(self, event=None):

        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.webp *.avif "
                    "*.bmp *.tif *.tiff *.gif *.ico",
                ),
                ("All Files", "*.*"),
            ],
        )

        if files:
            self.add_paths(files)

    # ========================================================
    # Select folder
    # ========================================================

    def select_folder(self):

        folder = filedialog.askdirectory(
            title="Select Image Folder",
        )

        if folder:
            self.add_paths([folder])

    # ========================================================
    # Add paths
    # ========================================================

    def add_paths(self, paths):

        added = 0

        for path_string in paths:

            path = Path(path_string)

            if path.is_dir():

                for file in path.rglob("*"):

                    if (
                        file.is_file()
                        and file.suffix.lower()
                        in SUPPORTED_INPUT_FORMATS
                    ):

                        if file not in self.files:

                            self.files.append(file)

                            added += 1

            elif path.is_file():

                if (
                    path.suffix.lower()
                    in SUPPORTED_INPUT_FORMATS
                ):

                    if path not in self.files:

                        self.files.append(path)

                        added += 1

        self.refresh_file_list()

        if added:

            self.write_log(
                f"Added {added} file(s)"
            )

    # ========================================================
    # Refresh file list
    # ========================================================

    def refresh_file_list(self):

        self.file_list.delete(
            0,
            "end",
        )

        for file in self.files:

            self.file_list.insert(
                "end",
                str(file),
            )

    # ========================================================
    # Clear files
    # ========================================================

    def clear_files(self):

        self.files.clear()

        self.refresh_file_list()

        self.write_log(
            "File list cleared"
        )

    # ========================================================
    # Open image
    # ========================================================

    def open_image(self, file):

        image = Image.open(file)

        image = ImageOps.exif_transpose(
            image
        )

        return image

    # ========================================================
    # Start conversion
    # ========================================================

    def start_conversion(self):

        if not self.files:

            messagebox.showwarning(
                "No Files",
                "Please add image files first.",
            )

            return

        try:

            quality = int(
                self.quality.get()
            )

            if not 1 <= quality <= 100:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Quality must be between 1 and 100.",
            )

            return

        width = None
        height = None

        if self.width.get().strip():

            try:

                width = int(
                    self.width.get()
                )

                if width <= 0:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Width must be a positive number.",
                )

                return

        if self.height.get().strip():

            try:

                height = int(
                    self.height.get()
                )

                if height <= 0:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Height must be a positive number.",
                )

                return

        if width is None and height is not None:

            messagebox.showerror(
                "Error",
                "Please enter Width first.",
            )

            return

        # Reset progress

        self.total_files = len(
            self.files
        )

        self.completed_files = 0
        self.converted_files = 0
        self.skipped_files = 0
        self.failed_files = 0

        self.progress["maximum"] = (
            self.total_files
        )

        self.progress["value"] = 0

        self.progress_percent.set(
            "0%"
        )

        self.progress_count.set(
            f"0 / {self.total_files} files"
        )

        self.current_file.set(
            "Starting..."
        )

        self.update_statistics()

        # Switch to progress tab

        self.notebook.select(
            self.progress_tab
        )

        self.start_button.configure(
            state="disabled"
        )

        threading.Thread(
            target=self.convert_files,
            args=(
                list(self.files),
                self.output_format.get(),
                quality,
                width,
                height,
                self.keep_aspect.get(),
            ),
            daemon=True,
        ).start()

    # ========================================================
    # Conversion worker
    # ========================================================

    def convert_files(
        self,
        files,
        output_format,
        quality,
        width,
        height,
        keep_aspect,
    ):

        extension = OUTPUT_FORMATS[
            output_format
        ]

        for file in files:

            self.root.after(
                0,
                lambda f=file.name:
                self.current_file.set(f)
            )

            try:

                if file.suffix.lower() == extension:

                    self.skipped_files += 1

                    self.write_log(
                        f"Skipping: {file.name}"
                    )

                else:

                    image = self.open_image(
                        file
                    )

                    # ------------------------------
                    # Resize
                    # ------------------------------

                    if width:

                        if keep_aspect:

                            image.thumbnail(
                                (
                                    width,
                                    height
                                    if height
                                    else width,
                                ),
                                Image.Resampling.LANCZOS,
                            )

                        else:

                            target_height = (
                                height
                                if height
                                else width
                            )

                            image = image.resize(
                                (
                                    width,
                                    target_height,
                                ),
                                Image.Resampling.LANCZOS,
                            )

                    # ------------------------------
                    # Convert color mode
                    # ------------------------------

                    save_image = image

                    if extension in (
                        ".jpg",
                        ".jpeg",
                        ".bmp",
                    ):

                        if save_image.mode != "RGB":

                            background = Image.new(
                                "RGB",
                                save_image.size,
                                "white",
                            )

                            if (
                                "A"
                                in save_image.getbands()
                            ):

                                background.paste(
                                    save_image,
                                    mask=save_image.getchannel(
                                        "A"
                                    ),
                                )

                            else:

                                background.paste(
                                    save_image
                                )

                            save_image = background

                    # ------------------------------
                    # Output filename
                    # ------------------------------

                    output = file.with_suffix(
                        extension
                    )

                    counter = 1

                    while output.exists():

                        output = file.with_name(
                            f"{file.stem}-{counter}"
                            f"{extension}"
                        )

                        counter += 1

                    # ------------------------------
                    # Save
                    # ------------------------------

                    save_kwargs = {}

                    if extension in (
                        ".jpg",
                        ".jpeg",
                        ".webp",
                        ".avif",
                    ):

                        save_kwargs["quality"] = (
                            quality
                        )

                    if extension == ".webp":

                        save_kwargs["method"] = 6

                    save_image.save(
                        output,
                        **save_kwargs,
                    )

                    self.converted_files += 1

                    self.write_log(
                        f"✓ {file.name} → "
                        f"{output.name}"
                    )

            except Exception as error:

                self.failed_files += 1

                self.write_log(
                    f"✗ {file.name}: {error}"
                )

            self.completed_files += 1

            self.update_progress_ui()

        self.root.after(
            0,
            self.conversion_finished,
        )

    # ========================================================
    # Progress UI
    # ========================================================

    def update_progress_ui(self):

        completed = (
            self.completed_files
        )

        total = self.total_files

        percent = int(
            completed / total * 100
        )

        self.root.after(
            0,
            lambda: self._update_progress(
                completed,
                total,
                percent,
            ),
        )

    def _update_progress(
        self,
        completed,
        total,
        percent,
    ):

        self.progress["value"] = completed

        self.progress_percent.set(
            f"{percent}%"
        )

        self.progress_count.set(
            f"{completed} / {total} files"
        )

        self.update_statistics()

    def update_statistics(self):

        self.stats_label.configure(
            text=(
                f"Converted: "
                f"{self.converted_files}    "
                f"Skipped: "
                f"{self.skipped_files}    "
                f"Failed: "
                f"{self.failed_files}"
            )
        )

    # ========================================================
    # Finished
    # ========================================================

    def conversion_finished(self):

        self.start_button.configure(
            state="normal"
        )

        self.current_file.set(
            "Finished"
        )

        self.write_log(
            "================================"
        )

        self.write_log(
            "Conversion completed"
        )

        self.write_log(
            f"Converted: "
            f"{self.converted_files}"
        )

        self.write_log(
            f"Skipped: "
            f"{self.skipped_files}"
        )

        self.write_log(
            f"Failed: "
            f"{self.failed_files}"
        )

        self.write_log(
            "================================"
        )

        messagebox.showinfo(
            "Finished",
            "Conversion completed.\n\n"
            f"Converted: {self.converted_files}\n"
            f"Skipped: {self.skipped_files}\n"
            f"Failed: {self.failed_files}",
        )

    # ========================================================
    # Log
    # ========================================================

    def write_log(self, message):

        self.root.after(
            0,
            lambda: self._write_log(
                message
            ),
        )

    def _write_log(self, message):

        self.log.configure(
            state="normal"
        )

        self.log.insert(
            "end",
            message + "\n"
        )

        self.log.see(
            "end"
        )

        self.log.configure(
            state="disabled"
        )


# ============================================================
# Application
# ============================================================

if __name__ == "__main__":

    root = TkinterDnD.Tk()

    app = ImageConverterApp(
        root
    )

    root.mainloop()