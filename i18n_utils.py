"""Internationalization utilities"""

import importlib
import os

# Global variable to hold the currently loaded messages
_MESSAGES = {}
_CURRENT_LANG = 'en' # Default language

def set_language(lang_code='en'):
    """Loads the message dictionary for the specified language code."""
    global _MESSAGES
    global _CURRENT_LANG
    
    # 調試模式開關
    DEBUG = False
    
    if DEBUG:
        print(f"[DEBUG i18n] 設置語言: {lang_code}")
    
    try:
        # 更新config模塊中的language屬性
        try:
            from nosqlmap_modules import config
            config.language = lang_code
            if DEBUG:
                print(f"[DEBUG i18n] 更新config.language: {config.language}")
        except ImportError:
            # 只有在程序啟動初始階段導入config模塊時可能會失敗
            if DEBUG:
                print(f"[DEBUG i18n] 無法導入config模塊")
            pass

        # Construct module path (e.g., lang.en)
        module_name = f"lang.{lang_code}"
        # Dynamically import the language module
        lang_module = importlib.import_module(module_name)
        # Get the MESSAGES dictionary from the module
        _MESSAGES = getattr(lang_module, 'MESSAGES', {})
        _CURRENT_LANG = lang_code
        return True
    except ModuleNotFoundError:
        print(f"Warning: Language file for '{lang_code}' not found. Falling back to English.")
        if lang_code != 'en': # Avoid infinite recursion if en.py is missing
            return set_language('en')
        return False
    except AttributeError:
        print(f"Warning: 'MESSAGES' dictionary not found in '{module_name}'. Falling back to English.")
        if lang_code != 'en':
            return set_language('en')
        return False
    except Exception as e:
        print(f"Error loading language '{lang_code}': {e}. Falling back to English.")
        if lang_code != 'en':
            return set_language('en')
        return False

def get_message(key, *args, **kwargs):
    """Gets the translated message for a given key and formats it.

    Args:
        key (str): The key for the message string.
        *args: Positional arguments for formatting the string (using .format()).
        **kwargs: Keyword arguments for formatting the string (using .format()).

    Returns:
        str: The translated and formatted message string, or the key itself
             if the translation is not found.
    """
    # Ensure messages are loaded (at least default English)
    if not _MESSAGES:
        set_language(_CURRENT_LANG)

    message = _MESSAGES.get(key, key) # Return key if translation not found

    try:
        # 嘗試使用位置參數格式化
        if args:
            return message.format(*args)
        # 否則嘗試使用關鍵字參數格式化
        else:
            return message.format(**kwargs)
    except KeyError as e:
        # Handle cases where a format key is missing in kwargs
        print(f"Warning: Missing format argument '{e}' for message key '{key}'.")
        return message # Return unformatted message
    except IndexError as e:
        # 處理位置參數索引超出範圍的情況
        print(f"Warning: Error formatting message key '{key}': Replacement index out of range for positional args tuple")
        return message
    except Exception as e:
        # Catch other potential formatting errors
        print(f"Warning: Error formatting message key '{key}': {e}")
        return message

# Initialize with default language on module load
set_language(_CURRENT_LANG) 