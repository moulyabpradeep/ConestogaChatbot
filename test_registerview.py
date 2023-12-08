import pytest
from registerview import RegisterView  # Assuming both files are in the same directory

def test_register_view_build():
    try:
        # Mocking the required callbacks for initialization
        def on_register_clicked():
            pass

        def on_back_clicked():
            pass

        # Create an instance of RegisterView
        register_view = RegisterView(on_register_clicked, on_back_clicked)

        # Call the build method
        register_view.build()

    except Exception as e:
        pytest.fail(f"Failed to execute RegisterView: {str(e)}")
