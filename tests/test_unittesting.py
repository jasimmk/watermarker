import pickle


from tests import WaterMarkUnitTestBase
from watermark.constants import RelativePosition
from watermark.job import job_function
from watermark.validator import *
from watermark.workflow import *


class FunctionTesting(WaterMarkUnitTestBase):
    def test_0101_color_testing(self):
        assert Color.TRANSPARENT == (0, 0, 0, 0)
        color_white = Color('white')
        assert color_white.get_dec_rgba() == (255, 255, 255, 255)
        # Setting black and getting back
        color_white.set_dec_rgba((0, 0, 0, 255))
        assert color_white.get_rgb() == (0, 0, 0)

    def test_0201_constant_testing(self):
        assert Position.TOP == 'TOP'
        assert Position.RIGHT == 'RIGHT'

        assert RelativePosition.TOP_LEFT == 'TOP_LEFT'
        assert RelativePosition.CENTER_CENTER == 'CENTER_CENTER'
        # all test

        assert all(x in RelativePosition.all() for x in ['CENTER_CENTER', 'BOTTOM_RIGHT', 'BOTTOM_CENTER'])
        assert all(x in (Position.TOP, Position.LEFT) for x in RelativePosition.split('TOP_LEFT'))
        with self.assertRaises(ValueError):
            RelativePosition.split('some_unknown_value')
        assert Size.AUTO is 0

    def test_0301_job_testing(self):
        wm_png_img = preprocess(self.get_watermark_png_with_alpha_file())
        wm_picked_png_img = pickle.dumps(wm_png_img)

        input_image_path = self.get_image_file()
        output_dir = self.get_output_dir()
        job_function(input_img_path=input_image_path, wm_img=wm_picked_png_img, output_dir=output_dir, output_size=[50])
        output_filename = os.path.join(self.get_output_dir(), self.get_image_filename())
        self.check_image_file(output_filename)
        # Delete file
        self.remove_file(output_filename)

        # Check CENTER_CENTER POSITION

        job_function(input_img_path=input_image_path, wm_img=wm_picked_png_img,
                     output_dir=output_dir, wm_position=RelativePosition.CENTER_CENTER)

        self.check_image_file(output_filename)
        # Delete file
        self.remove_file(output_filename)

        # Check CENTER_LEFT POSITION
        job_function(input_img_path=input_image_path, wm_img=wm_picked_png_img,
                     output_dir=output_dir, wm_position=RelativePosition.CENTER_LEFT)

        # Check TOP_RIGHT POSITION
        job_function(input_img_path=input_image_path, wm_img=wm_picked_png_img,
                     output_dir=output_dir, wm_position=RelativePosition.TOP_RIGHT)

        self.check_image_file(output_filename)
        # Delete file
        self.remove_file(output_filename)

        # Checking only resize
        job_function(input_img_path=input_image_path,
                     output_dir=output_dir, output_size=(800, 600))

        self.check_image_file(output_filename)
        self.remove_file(output_filename)


        # Checking text with CENTER_CENTER
        job_function(input_img_path=input_image_path, wm_img=wm_picked_png_img,
                     output_dir=output_dir, wm_position=RelativePosition.CENTER_CENTER)

        self.check_image_file(output_filename)
        self.remove_file(output_filename)

        # Resize to 800x600
        wm_picked_png_img = create_text_image(img_width=800, img_height=600, text="WIKIPEDIA")
        wm_picked_png_img = pickle.dumps(wm_picked_png_img)

        job_function(input_img_path=input_image_path, wm_img=wm_picked_png_img,
                     output_dir=output_dir, output_format='png',
                     output_size=(800, 600))

        output_filename = output_filename.replace('.jpg', '.png')
        self.check_image_file(output_filename)
        self.remove_file(output_filename)

        # Checking only conversion
        job_function(input_img_path=input_image_path,
                     output_dir=output_dir, output_format='png')

        self.check_image_file(output_filename)
        self.remove_file(output_filename)

        # Checking bad transparency issues, for watermark images without alpha transparency
        wm_jpg_img = preprocess(self.get_watermark_jpg_file())
        wm_picked_jpg_img = pickle.dumps(wm_jpg_img)
        job_function(input_img_path=input_image_path, wm_img=wm_picked_jpg_img,
                     output_dir=output_dir, output_format='png', raise_errors=True)

        self.check_image_file(output_filename)
        self.remove_file(output_filename)

    def test_0401_validators(self):
        # Font validator

        fv = FontValidator()
        assert fv(None) in DEFAULT_FONTS
        with self.assertRaises(argparse.ArgumentTypeError):
            fv('non_existing')

        # Color validator
        cv = ColorValidator()
        assert cv('white') == (255, 255, 255, 255)
        with self.assertRaises(argparse.ArgumentTypeError):
            cv('non_existing')
        assert cv('transparent') == (0, 0, 0, 0)
