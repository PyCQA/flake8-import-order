# smarkets
import ast
# This comment should not prevent the I201 below, it is not a newline.
import X # I201
import flake8_import_order # I201
if TYPE_CHECKING:
    import ast # I300
    # This comment should not prevent the I201 below, it is not a newline.
    import X # I201
    import flake8_import_order # I201
