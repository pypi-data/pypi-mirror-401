from typing import Optional, Dict, Any
import logging

# Configure basic logging
logger = logging.getLogger(__name__)

class WdaExists:
    """
    Replicates the behavior of the `Exists` class from uiautomator2.
    """

    def __init__(self, driver: Any, selector: Dict[str, Any]):
        self.d = driver
        self.selector = selector

    def __bool__(self) -> bool:
        """
        Handles the case: `if d(..).exists:` (without parentheses).
        Checks immediately without waiting.
        """
        try:
            # The .exists property in WDA returns True/False
            return bool(self.d(**self.selector).exists)
        except Exception:
            return False

    def __call__(self, timeout: float = 0) -> bool:
        """
        Handles the case: `if d(..).exists():` or `if d(..).exists(timeout=5):`.
        """
        if timeout > 0:
            # If timeout is provided, behavior is equivalent to .wait()
            try:
                self.d(**self.selector).wait(timeout=timeout)
                return True
            except Exception:
                return False

        # If no timeout (timeout=0), behavior is equivalent to reading the property directly
        return bool(self)

    def __repr__(self) -> str:
        return str(bool(self))


class WdaAdapter:
    """
    WDA Adapter: Maps uiautomator2 syntax to facebook-wda.
    """

    def __init__(self, wda_driver: Any):
        self.d = wda_driver  # wda session

    def __call__(self, **kwargs: Any) -> 'WdaElement':
        """
        Intercepts `d(text="...")` calls and returns a disguised WdaElement.
        """
        # 1. Handle Android EditText -> Wda TextField/SecureTextField
        if kwargs.get('className') == 'android.widget.EditText':
            # iOS splits input fields into text fields and secure text fields.
            # Using OR syntax to find both.
            # Note: wda predicate syntax
            kwargs = {
                'predicate': 'type == "XCUIElementTypeTextField" OR type == "XCUIElementTypeSecureTextField"'
            }

        if kwargs.get('scrollable'):
            # Common scrolling containers in iOS: Table, ScrollView, CollectionView, WebView
            kwargs = {
                'predicate': 'type == "XCUIElementTypeTable" OR type == "XCUIElementTypeScrollView" OR type == "XCUIElementTypeCollectionView" OR type == "XCUIElementTypeWebView"'
            }

        return WdaElement(self.d, **kwargs)

    def xpath(self, xpath_str: str) -> 'WdaElement':
        """
        Finds an element by XPath, with automatic adjustments for iOS.
        """
        # Replace Android's @text with iOS's @label
        if "@text" in xpath_str:
            # logger.warning("Automatically replacing @text with @label in XPath for iOS compatibility")
            xpath_str = xpath_str.replace("@text", "@label")

        # Handle content-desc (Android) -> name (iOS)
        if "@content-desc" in xpath_str:
            xpath_str = xpath_str.replace("@content-desc", "@name")

        return WdaElement(self.d, xpath=xpath_str)

    def app_start(self, bundle_id: str) -> None:
        """Launches an application by bundle ID."""
        self.d.app_launch(bundle_id)

    def app_stop(self, bundle_id: str) -> None:
        """Terminates an application by bundle ID."""
        self.d.app_terminate(bundle_id)

    def press(self, key: str) -> None:
        """Simulates a key press."""
        # Simple mapping for the home key
        if key == "home":
            self.d.home()

    def send_keys(self, text: str) -> None:
        """
        Simulates u2's d.send_keys(text).
        """
        self.d.send_keys(text)

    def dump_hierarchy(self, compressed: bool = False, pretty: bool = False, max_depth: Optional[int] = None) -> Any:
        """
        Simulates Android's dump_hierarchy, actually calling WDA source.
        """
        return self.d.source()


class WdaElement:
    def __init__(self, driver: Any, index: Optional[int] = None, **kwargs: Any):
        self.d = driver
        self.kwargs = kwargs
        self.index = index  # If None, matches the first of all; if set, specifies the index
        self.selector = self._map_selector(kwargs)

    def _map_selector(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core mapping logic: u2 arguments -> wda arguments.
        """
        # 1. XPath pass-through
        if 'xpath' in kwargs:
            return {'xpath': kwargs['xpath']}

        # 2. Text full match -> Predicate (label == 'xxx')
        if 'text' in kwargs:
            return {'predicate': f"label == '{kwargs['text']}'"}

        # 3. Text contains -> Predicate (label LIKE '*xxx*')
        if 'textContains' in kwargs:
            return {'predicate': f"label LIKE '*{kwargs['textContains']}*'"}

        # 4. ResourceId -> Name
        if 'resourceId' in kwargs:
            return {'name': kwargs['resourceId']}

        # 5. ClassName -> ClassName
        if 'className' in kwargs:
            return {'className': kwargs['className']}

        # 6. Description -> Name or Label (Depends on App implementation, usually mapped to label/name)
        if 'description' in kwargs:
            return {'predicate': f"name == '{kwargs['description']}'"}

        return kwargs

    def _get_wda_element(self) -> Any:
        """Internal method: Get the real WDA element object."""
        if self.index is not None:
            # If an index is specified (e.g., edit_texts[0])
            # wda find returns a list, take the corresponding index
            elements = self.d(**self.selector).find_elements()
            if len(elements) > self.index:
                return elements[self.index]
            raise IndexError(f"Element index {self.index} out of range")
        else:
            # Default case, return the first match
            return self.d(**self.selector)

    def __len__(self) -> int:
        """
        Simulates u2's len(d(class="..."))
        Returns the number of matching elements.
        """
        # wda's find_elements() returns a list of all matches
        return len(self.d(**self.selector).find_elements())

    def __getitem__(self, index: int) -> 'WdaElement':
        """
        Simulates u2's edit_texts[0]
        Returns a new WdaElement instance bound to a specific index.
        """
        # Pass the same driver and kwargs, but lock the index
        return WdaElement(self.d, index=index, **self.kwargs)

    @property
    def text(self) -> str:
        """
        Adapts u2.xpath(...).wait().text
        WDA text retrieval is usually .label or .text
        """
        try:
            # If it's a wda element found via xpath
            return self.d(**self.selector).get().label
        except Exception:
            return ""

    def get(self, timeout: Optional[float] = None) -> 'WdaElement':
        """
        Simulates u2's .get()
        In u2, it returns specific object info.
        Here it returns self, as self already has the text property implementation.
        """
        if timeout:
            self.wait(timeout=timeout)

        # Ensure the element actually exists, as wda might raise an error if not
        if not self.exists:
            # If strict consistency is required, an exception could be raised here
            pass

        return self

    def click(self, timeout: Optional[float] = None) -> None:
        el = self._get_wda_element()
        # If it's a single element object (wda Element), click directly
        # If it's a Selector (default), need to wait
        if hasattr(el, 'wait'):
            el.wait(timeout=timeout if timeout else 5).click()
        else:
            el.click()

    def clear_text(self) -> None:
        """Simulates .clear_text()"""
        el = self._get_wda_element()
        # WDA Selector doesn't have clear_text, must resolve to Element first
        if hasattr(el, 'wait'):
            el = el.wait(timeout=5)
        el.clear_text()

    def click_exists(self, timeout: float = 0) -> bool:
        """
        Custom extension: If exists, click and return True, else return False.
        """
        try:
            # Try waiting for appearance
            el = self.d(**self.selector).wait(timeout=timeout)
            if el:
                el.click()
                return True
            return False
        except Exception:
            return False

    @property
    def exists(self) -> WdaExists:
        return WdaExists(self.d, self.selector)

    def wait(self, timeout: float = 10) -> bool:
        """
        Standard element wait (e.g., d(text='...').wait())
        u2 natively returns bool here.
        """
        try:
            self.d(**self.selector).wait(timeout=timeout)
            return True
        except Exception:
            return False

    def get_text(self) -> str:
        """Simulates u2's .get_text()"""
        try:
            return self.d(**self.selector).get().label
        except Exception:
            return ""

    def set_text(self, text: str) -> None:
        """Simulates u2's .set_text()"""
        el = self.d(**self.selector).wait(timeout=5)
        el.clear_text()
        el.set_text(text)

    @property
    def info(self) -> Dict[str, Any]:
        """Simulates u2's .info"""
        el = self.d(**self.selector).get()
        return {
            "text": el.label,
            "bounds": el.bounds,  # wda returns Rect(x,y,w,h)
            "className": el.className,
            "resourceId": el.name
        }
