if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QSystemTrayIcon
    from PySide6.QtGui import QIcon
    from PySide6.QtCore import QTimer
    import git_icon_rc
    import sys
    print (sys.argv)
    app = QApplication()

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("Systray", "I couldn't detect any system tray on this system.")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(
        prog="git notifier",
        description="send a notification message to the operating system"
        )
    parser.add_argument("--title", type=str, default="")
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--icon", type=str, default="info")
    parser.add_argument("--duration", type=int, default=5, help="duration in seconds")
    args=parser.parse_args(sys.argv[1:])
    icons=dict(
        i=QSystemTrayIcon.MessageIcon.Information,
        w=QSystemTrayIcon.MessageIcon.Warning,
        c=QSystemTrayIcon.MessageIcon.Critical
    )
    tray_icon=QSystemTrayIcon(app)
    msg_icon=icons.get(args.icon[0].lower(),QSystemTrayIcon.MessageIcon.Information)
    icon=QIcon(u":/git-icon/Git-Icon-1788C.png")
    tray_icon.setIcon(icon)
    tray_icon.setVisible(True)
    tray_icon.showMessage(args.title,args.text,msg_icon)

    QTimer.singleShot(abs(int(args.duration*1000)),app.quit)
    sys.exit(app.exec())