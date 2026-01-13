import unittest
from unittest.mock import MagicMock, call

from u2_adapter import WdaAdapter, WdaElement, WdaExists


class TestWdaAdapter(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.adapter = WdaAdapter(self.mock_driver)

    def test_call_with_text(self):
        # Test d(text="Settings")
        element = self.adapter(text="Settings")
        self.assertIsInstance(element, WdaElement)
        self.assertEqual(element.selector, {"predicate": "label == 'Settings'"})

    def test_call_with_resource_id(self):
        # Test d(resourceId="btn_login")
        element = self.adapter(resourceId="btn_login")
        self.assertEqual(element.selector, {"name": "btn_login"})

    def test_call_with_android_edittext(self):
        # Test mapping android.widget.EditText
        element = self.adapter(className="android.widget.EditText")
        expected_predicate = 'type == "XCUIElementTypeTextField" OR type == "XCUIElementTypeSecureTextField"'
        self.assertEqual(element.selector["predicate"], expected_predicate)

    def test_xpath_conversion(self):
        # Test xpath conversion
        element = self.adapter.xpath('//android.widget.Button[@text="Login"]')
        self.assertEqual(
            element.selector["xpath"], '//android.widget.Button[@label="Login"]'
        )

        element = self.adapter.xpath('//*[@content-desc="desc"]')
        self.assertEqual(element.selector["xpath"], '//*[@name="desc"]')

    def test_element_click(self):
        # Test clicking an element
        mock_el = MagicMock()
        # Mock the chain: d(..).wait().click()
        self.mock_driver.return_value.wait.return_value = mock_el

        self.adapter(text="Login").click()

        # Verify driver was called with correct predicate
        self.mock_driver.assert_called_with(predicate="label == 'Login'")
        # Verify wait was called
        self.mock_driver.return_value.wait.assert_called()
        # Verify click was called on the result of wait
        mock_el.click.assert_called_once()

    def test_element_exists_property(self):
        # Test if d(..).exists returns boolean
        self.mock_driver.return_value.exists = True
        exists = self.adapter(text="Settings").exists
        # .exists returns a WdaExists object
        self.IsInstance(exists, WdaExists)
        # Casting to bool should trigger the check
        self.assertTrue(bool(exists))

    def test_element_exists_call(self):
        # Test if d(..).exists() returns boolean
        # Case 1: Timeout > 0 (wait)
        self.mock_driver.return_value.wait.return_value = True
        self.assertTrue(self.adapter(text="Settings").exists(timeout=1))

        # Case 2: Timeout = 0 (check immediately)
        self.mock_driver.return_value.exists = False
        self.assertFalse(self.adapter(text="Settings").exists(timeout=0))

    def test_app_management(self):
        self.adapter.app_start("com.example.app")
        self.mock_driver.app_launch.assert_called_with("com.example.app")

        self.adapter.app_stop("com.example.app")
        self.mock_driver.app_terminate.assert_called_with("com.example.app")

    def IsInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))


if __name__ == "__main__":
    unittest.main()
    # export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python3 -m unittest discover tests
