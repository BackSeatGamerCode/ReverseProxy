import source.screens.main as main
import source.error_manager as error_manager


if __name__ == '__main__':
    try:
        main.show()
    except (KeyboardInterrupt, SystemExit):
        pass

    except Exception:
        error_manager.dump_error()
