from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest
from unittest.mock import Mock

from PIL import Image

from image_converter_gui import ImageConverterApp, OUTPUT_FORMATS


class OutputFilenameTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.app = ImageConverterApp.__new__(ImageConverterApp)
        self.app.root = Mock()
        self.app.refresh_file_list = Mock()
        self.app.update_progress_ui = Mock()
        self.app.write_log = Mock()
        self.app.files = []
        self.app.completed_files = 0
        self.app.converted_files = 0
        self.app.skipped_files = 0
        self.app.failed_files = 0

    def make_image(self, path):
        with Image.new("RGB", (32, 32), "red") as image:
            image.save(path)
        return path

    def convert(self, files, output_format):
        self.app.convert_files(files, output_format, 85, None, None, True)
        self.assertEqual(self.app.completed_files, len(files))
        self.assertEqual(self.app.converted_files, len(files))
        self.assertEqual(self.app.skipped_files, 0)
        self.assertEqual(self.app.failed_files, 0)
        self.assertEqual(self.app.update_progress_ui.call_count, len(files))

    def test_uses_original_stem_for_every_output_format(self):
        source = self.make_image(self.directory / "image.test.tiff")

        for output_format, extension in OUTPUT_FORMATS.items():
            with self.subTest(output_format=output_format):
                self.app.completed_files = 0
                self.app.converted_files = 0
                self.app.update_progress_ui.reset_mock()
                self.convert([source], output_format)
                suffix = "_01" if extension == source.suffix else ""
                output = self.directory / f"image.test{suffix}{extension}"
                with Image.open(output) as image:
                    image.load()
                    self.assertEqual(image.format, Image.registered_extensions()[extension])

    def test_existing_source_and_numbered_outputs_are_preserved(self):
        existing = [
            self.make_image(self.directory / name)
            for name in ("image.avif", "image_01.avif", "image_02.avif")
        ]
        original_bytes = {file: file.read_bytes() for file in existing}

        self.convert([existing[0]], "AVIF")

        output = self.directory / "image_03.avif"
        with Image.open(output) as image:
            image.load()
            self.assertEqual(image.format, "AVIF")
        for file, contents in original_bytes.items():
            self.assertEqual(file.read_bytes(), contents)

    def test_batch_reserves_names_in_each_subfolder(self):
        for folder in ("first", "second"):
            subfolder = self.directory / folder
            subfolder.mkdir()
            self.make_image(subfolder / "image.bmp")
            self.make_image(subfolder / "image.png")

        self.app.add_paths([str(self.directory)])
        self.assertEqual(len(self.app.files), 4)
        self.convert(self.app.files, "WebP")

        for folder in ("first", "second"):
            self.assertEqual(
                sorted(path.name for path in (self.directory / folder).glob("*.webp")),
                ["image.webp", "image_01.webp"],
            )

    def test_concurrent_saves_reserve_distinct_names_before_writing(self):
        source = self.directory / "image.jpg"
        both_reserved = Barrier(2, timeout=5)

        def save_image(stream, *, format):
            both_reserved.wait()
            with Image.new("RGB", (32, 32)) as image:
                image.save(stream, format=format)

        image = Mock()
        image.save.side_effect = save_image
        with ThreadPoolExecutor(max_workers=2) as executor:
            saves = [
                executor.submit(self.app.save_with_unique_name, image, source, ".png")
                for _ in range(2)
            ]
            outputs = {save.result() for save in saves}

        self.assertEqual(
            outputs, {self.directory / "image.png", self.directory / "image_01.png"}
        )
        for output in outputs:
            with Image.open(output) as saved:
                saved.load()

    def test_failed_save_removes_partial_output(self):
        source = self.directory / "image.jpg"
        existing = self.make_image(self.directory / "image.png")
        original_bytes = existing.read_bytes()

        def fail_after_write(stream, *, format):
            stream.write(b"partial image")
            raise OSError("save failed")

        image = Mock()
        image.save.side_effect = fail_after_write
        with self.assertRaisesRegex(OSError, "save failed"):
            self.app.save_with_unique_name(image, source, ".png")

        self.assertEqual(existing.read_bytes(), original_bytes)
        self.assertFalse((self.directory / "image_01.png").exists())
