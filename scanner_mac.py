import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
from datetime import datetime
import os
import platform

scanned_codes = set()
code_list = []
progress_file = 'progress.csv'


# Загружаем сохранённый прогресс, если файл существует
if os.path.exists(progress_file):
    try:
        df_progress = pd.read_csv(progress_file)
        code_list = df_progress['Код'].astype(str).tolist()
        scanned_codes = set(code_list)
    except Exception as e:
        messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить сохранённый прогресс:\n{e}")


def play_success_sound():
    os.system('afplay /System/Library/Sounds/Glass.aiff')


def play_error_sound():
    os.system('afplay /System/Library/Sounds/Basso.aiff')


# Функция проверки и реакции на код
def check_code(event=None):
    code = entry.get().strip()
    if not code:
        return

    if code in scanned_codes:
        result_label.config(text=f"⚠️ ДУБЛИКАТ: {code}", fg="red")
        play_error_sound()
    else:
        scanned_codes.add(code)
        code_list.append(code)
        result_label.config(text=f"✅ Новый код: {code}", fg="green")
        scanned_box.insert(tk.END, code + '\n')
        scanned_box.see(tk.END)
        play_success_sound()
        save_progress()

    entry.delete(0, tk.END)


# Сохраняем текущий прогресс в файл
def save_progress():
    df = pd.DataFrame({'Код': code_list})
    df.to_csv(progress_file, index=False)


def save_to_excel():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"отсканированные_{current_time}.xlsx"
    df = pd.DataFrame({'Код': code_list})
    df.to_excel(filename, index=False)
    messagebox.showinfo("Сохранено", f"Список сохранён в '{filename}'")


def delete_code():
    try:
        selected_code = scanned_box.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        if selected_code in scanned_codes:
            scanned_codes.remove(selected_code)
            code_list.remove(selected_code)
            update_scanned_box()
            save_progress()
            result_label.config(text=f"🗑️ Код {selected_code} удалён", fg="orange")
        else:
            messagebox.showerror("Ошибка", "Код не найден.")
    except tk.TclError:
        messagebox.showerror("Ошибка", "Выделите код для удаления.")


def update_scanned_box():
    scanned_box.delete(1.0, tk.END)
    for code in code_list:
        scanned_box.insert(tk.END, code + '\n')
    scanned_box.see(tk.END)


# GUI
root = tk.Tk()
root.title("Сканирование QR-кодов")
root.geometry("400x500")

entry = tk.Entry(root, font=('Arial', 18))
entry.pack(pady=10)
entry.focus()

btn = tk.Button(root, text="Проверить код", command=check_code, font=('Arial', 14))
btn.pack()

result_label = tk.Label(root, text="", font=('Arial', 14))
result_label.pack(pady=10)

scanned_box = scrolledtext.ScrolledText(root, height=15, font=('Courier', 12))
scanned_box.pack(pady=10, fill=tk.BOTH, expand=True)

# Заполняем при запуске, если есть старые коды
update_scanned_box()

delete_btn = tk.Button(root, text="Удалить выбранный код", command=delete_code, font=('Arial', 12))
delete_btn.pack(pady=5)

save_btn = tk.Button(root, text="Сохранить в Excel", command=save_to_excel, font=('Arial', 12))
save_btn.pack(pady=5)

root.bind('<Return>', check_code)
root.mainloop()
