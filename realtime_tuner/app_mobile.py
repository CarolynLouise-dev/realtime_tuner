import flet as ft
import threading
import time

# --- IMPORT NGUYÊN XI TỪ FILE MAIN CỦA CẬU ---
try:
    from audio.audio_stream import start_stream, get_frame, FS
    from core.pitch import detect_pitch
    from core.note_mapper import freq_to_note
except ImportError:
    print("⚠️ Hãy đảm bảo chạy file này ở thư mục gốc của dự án (realtime_tuner/)")


def main(page: ft.Page):
    # Cấu hình giao diện Mobile cơ bản
    page.title = "Guitar Tuner"
    page.window.width = 380
    page.window.height = 700
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 1. Các thành phần hiển thị
    note_txt = ft.Text("--", size=100, weight="bold", color="white")
    cents_txt = ft.Text("+0.00 cents", size=20, color="green")
    hz_txt = ft.Text("0.00 Hz", size=18, color="grey")

    # Biến trạng thái để điều khiển vòng lặp
    state = {"is_running": False}

    # 2. Vòng lặp Tuner (Bê nguyên logic While True vào đây)
    def tuner_worker():
        stream = start_stream()
        last_update_time = 0

        while state["is_running"]:
            frame = get_frame()
            if frame is None:
                continue

            # CHỐNG SAI: Đảm bảo truyền FS từ audio_stream vào đây
            pitch = detect_pitch(frame, fs=FS)

            if pitch:
                # CHỐNG CHẬM: Chỉ cập nhật UI tối đa 10 lần/giây (0.1s)
                # Việc cập nhật 100 lần/giây qua Wifi sẽ làm treo app
                current_time = time.time()
                if current_time - last_update_time > 0.1:
                    note, cents = freq_to_note(pitch)

                    note_txt.value = note
                    cents_txt.value = f"{float(cents):+.2f} cents"
                    hz_txt.value = f"{pitch:.2f} Hz"
                    cents_txt.color = "green" if abs(float(cents)) < 5 else "orange"

                    page.update()
                    last_update_time = current_time

            # Nghỉ một chút để giải phóng CPU cho việc truyền tải dữ liệu qua Wifi
            time.sleep(0.01)

    # 3. Hàm xử lý nút Bấm
    def on_click_toggle(e):
        if not state["is_running"]:
            state["is_running"] = True
            btn.text = "STOP TUNER"
            btn.bgcolor = "red"
            # Chạy vòng lặp trong một Thread riêng để không làm treo UI
            threading.Thread(target=tuner_worker, daemon=True).start()
        else:
            state["is_running"] = False
            btn.text = "START TUNER"
            btn.bgcolor = "green"
        page.update()

    # 4. Nút bấm điều khiển
    btn = ft.ElevatedButton(
        text="START TUNER",
        on_click=on_click_toggle,
        bgcolor="green",
        color="white",
        width=200,
        height=50
    )

    # 5. Sắp xếp giao diện
    page.add(
        ft.Column(
            [
                ft.Text("GUITAR TUNER PRO", size=16, weight="bold", color="grey"),
                ft.Container(height=20),
                note_txt,
                cents_txt,
                hz_txt,
                ft.Container(height=40),
                btn
            ],
            horizontal_alignment="center",
        )
    )


if __name__ == "__main__":
    # Ép chạy Web View để chắc chắn hiện giao diện trên Mac
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)