import gphoto2 as gp
import sys

def list_config():
    context = gp.Context()
    camera = gp.Camera()
    try:
        camera.init(context)
    except Exception as e:
        print("Failed to init:", e)
        return
    
    config = camera.get_config(context)
    
    def print_config(widget, depth=0):
        name = widget.get_name()
        try:
            value = widget.get_value()
        except:
            value = "<no value>"
        print("  " * depth + f"{name}: {value}")
        for n in range(widget.count_children()):
            print_config(widget.get_child(n), depth + 1)
            
    print_config(config)
    camera.exit(context)

if __name__ == "__main__":
    list_config()
