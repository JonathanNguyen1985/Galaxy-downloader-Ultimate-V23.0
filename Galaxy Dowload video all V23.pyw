import customtkinter as ctk
import yt_dlp
import threading
import time
import random
from tkinter import filedialog, ttk, messagebox
import os
import webbrowser
import requests  
import socket    

# --- JONATHAN GALAXY V23.0 - DOWNLOADER EDITION ---
# Tác giả: JONATHAN NGUYỄN
# Cập nhật: TỐI GIẢN HÓA SIÊU NHẸ - ONLY DOWNLOADER

AUTHOR = "JONATHAN NGUYỄN"
CYAN = "#00f2ff"
MAGENTA = "#ff00ff"
BG_DARK = "#0b0e14"
CARD_BG = "#161b22"
HOVER_BG = "#21262d"

ctk.set_appearance_mode("Dark")

class JonathanGalaxyMonster(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"V23.0 GALAXY ULTIMATE - DOWNLOADER EDITION | BY {AUTHOR}")
        self.geometry("1550x900")
        self.configure(fg_color=BG_DARK)
        
        # --- HỆ THỐNG ĐƯỜNG DẪN TỰ ĐỘNG ---
        base_p = os.path.join(os.path.expanduser("~"), "Downloads")
        self.paths = {
            'dl': os.path.join(base_p, "Jonathan_Downloads")
        }
        for p in self.paths.values():
            os.makedirs(p, exist_ok=True)

        self.video_list = {}
        self.all_selected = True 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_styles()
        
        self.show_splash_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=CARD_BG, foreground="white", fieldbackground=CARD_BG, rowheight=35, borderwidth=0)
        style.map("Treeview", background=[('selected', CYAN)], foreground=[('selected', 'black')])
        style.configure("Treeview.Heading", background="#21262d", foreground=CYAN, font=("Arial", 10, "bold"))

    def open_facebook(self, event):
        webbrowser.open_new("https://www.facebook.com/jonathanNguyen421985")

    def log_to_galaxy_cloud(self, title, url, status):
        def send_task():
            try:
                api_url = "https://script.google.com/macros/s/AKfycbz9NCcuTgJwrKfgoaEhS2CW-HFvumvwIqiM5LKexUW6eLFsbExhCxqC95ff8--qR5RPMQ/exec"
                pc_name = socket.gethostname() 
                payload = {
                    "user": pc_name,
                    "title": title,
                    "url": url,
                    "status": status
                }
                requests.post(api_url, json=payload, timeout=10)
            except:
                pass 
        threading.Thread(target=send_task, daemon=True).start()

    def show_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self, fg_color="#050505", corner_radius=0)
        self.splash_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self.splash_frame, text="JONATHAN NGUYỄN", font=("Orbitron", 60, "bold"), text_color=CYAN).pack(expand=True, pady=(120, 0))
        ctk.CTkLabel(self.splash_frame, text="Bản Galaxy Ultimate V23.0 Downloader", font=("Arial", 25, "bold"), text_color=MAGENTA).pack(pady=10)
        
        info_frame = ctk.CTkFrame(self.splash_frame, fg_color="transparent")
        info_frame.pack(pady=20)
        
        ctk.CTkLabel(info_frame, text="Chào Mừng Các Bạn . Chúc Các Bạn Một Ngày Làm Việc Vui Vẻ", font=("Arial", 16), text_color="white").pack(pady=8)
        ctk.CTkLabel(info_frame, text="© Bản Quyền Thuộc : Jonathan Nguyễn", font=("Arial", 15, "bold"), text_color="yellow").pack(pady=5)
        
        contact_frame = ctk.CTkFrame(info_frame, fg_color="#161b22", corner_radius=10, border_width=1, border_color="#30363d")
        contact_frame.pack(pady=15, ipadx=20, ipady=10)
        
        ctk.CTkLabel(contact_frame, text="📞 Liên Hệ Zalo : 0377030001", font=("Arial", 14, "bold"), text_color=CYAN).pack(pady=2)
        ctk.CTkLabel(contact_frame, text="🌐 Facebook : https://www.facebook.com/jonathanNguyen421985", font=("Arial", 14), text_color=CYAN).pack(pady=2)

        self.splash_status = ctk.CTkLabel(self.splash_frame, text="Đang kết nối thuật toán Downloader...", font=("Arial", 14), text_color="#8b949e")
        self.splash_status.pack(pady=(30, 10))
        
        self.splash_prog = ctk.CTkProgressBar(self.splash_frame, width=500, height=15, fg_color="#1c2128", progress_color=CYAN, mode="indeterminate")
        self.splash_prog.pack(pady=10)
        self.splash_prog.start()

        self.after(2000, lambda: self.splash_status.configure(text="Khởi tạo thành công! Sẵn sàng làm việc..."))
        self.after(3500, self.destroy_splash_and_load_main)

    def destroy_splash_and_load_main(self):
        self.splash_prog.stop()
        self.splash_frame.destroy()
        self.init_ui()

    def update_btn_state(self, btn, status_lab, prog, is_running, start_text="THỰC HIỆN", color=MAGENTA):
        if is_running:
            btn.configure(state="disabled", text="⏳ ĐANG XỬ LÝ...", fg_color="#444444")
            status_lab.configure(text="Trạng thái: Đang thực thi nhiệm vụ...", text_color=MAGENTA)
            prog.start()
        else:
            btn.configure(state="normal", text=start_text, fg_color=color)
            status_lab.configure(text="Trạng thái: Hoàn tất nhiệm vụ!", text_color=CYAN)
            prog.stop()

    def init_ui(self):
        # 1. SIDEBAR (Đã xóa text JONATHAN NGUYỄN thô)
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=CARD_BG, border_width=1, border_color="#30363d")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(2, weight=1) 
        
        ctk.CTkLabel(self.sidebar, text="Galaxy ULTIMATE V23.0 PRO", font=("Arial", 13, "bold"), text_color=MAGENTA).pack(pady=(50, 5))
        
        link = ctk.CTkLabel(self.sidebar, text="( LIÊN HỆ : Facebook )", font=("Arial", 10, "underline"), text_color="#8b949e", cursor="hand2")
        link.pack(pady=(0, 30))
        link.bind("<Button-1>", self.open_facebook)
        
        self.nav_buttons = []
        menu_items = [
            ("📥  VIBE DOWNLOADER", 0)
        ]

        for text, index in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", text_color="#8b949e", anchor="w", height=45, hover_color=HOVER_BG, corner_radius=8, font=("Segoe UI", 13, "bold"), command=lambda i=index: self.select_tab(i))
            btn.pack(fill="x", padx=15, pady=2)
            self.nav_buttons.append(btn)

        # 2. MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        self.tab_frames = []
        for _ in range(1): # Chỉ còn 1 tab
            frame = ctk.CTkFrame(self.main_container, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color="#30363d")
            self.tab_frames.append(frame)
        
        self.tab_dl = self.tab_frames[0]

        self.setup_dl_tab()
        self.select_tab(0)

    def select_tab(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(fg_color=CYAN, text_color="black", hover_color=CYAN)
            else:
                btn.configure(fg_color="transparent", text_color="#8b949e", hover_color=HOVER_BG)
        for i, frame in enumerate(self.tab_frames):
            if i == index:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def update_path_entry(self, k, entry_widget):
        p = filedialog.askdirectory()
        if p:
            self.paths[k] = p
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, p)

    # ==========================================
    # TAB 1: VIBE DOWNLOADER
    # ==========================================
    def setup_dl_tab(self):
        container = ctk.CTkFrame(self.tab_dl, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=25)
        
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x")
        self.url_input = ctk.CTkEntry(header, placeholder_text="Dán link hoặc nạp file .txt (Dailymotion, Youtube, FB, Insta)...", height=50, border_color=CYAN, font=("Segoe UI", 13))
        self.url_input.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        ctk.CTkButton(header, text="📂 TXT", width=80, height=50, fg_color="#30363d", command=self.import_txt).pack(side="left", padx=5)
        self.btn_scan = ctk.CTkButton(header, text="QUÉT DỮ LIỆU", width=150, height=50, fg_color=CYAN, text_color="black", font=("Arial", 13, "bold"), command=self.start_scan)
        self.btn_scan.pack(side="left")
        
        dl_path_f = ctk.CTkFrame(container, fg_color="transparent")
        dl_path_f.pack(fill="x", pady=(10, 0))
        self.dl_path_entry = ctk.CTkEntry(dl_path_f, height=35, border_color="#30363d", fg_color="#0d1117")
        self.dl_path_entry.insert(0, self.paths['dl'])
        self.dl_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(dl_path_f, text="NƠI LƯU", width=100, height=35, command=lambda: self.update_path_entry('dl', self.dl_path_entry)).pack(side="right")

        cfg = ctk.CTkFrame(container, fg_color="#1c2128", corner_radius=12)
        cfg.pack(fill="x", pady=15)
        inner = ctk.CTkFrame(cfg, fg_color="transparent")
        inner.pack(expand=True, pady=10)
        
        self.res_menu = ctk.CTkOptionMenu(inner, values=["4K (2160p)", "2K (1440p)", "1080p", "720p", "480p", "360p"], width=130)
        self.res_menu.set("1080p")
        self.res_menu.pack(side="left", padx=10)
        
        self.mode_menu = ctk.CTkOptionMenu(inner, values=["Video MP4 + Ảnh JPG", "Chỉ Video MP4", "Chỉ MP3", "Chỉ Ảnh JPG"], width=190, fg_color=MAGENTA)
        self.mode_menu.pack(side="left", padx=10)
        
        ctk.CTkLabel(inner, text="GIỚI HẠN SỐ LƯỢNG:").pack(side="left", padx=5)
        self.limit_val = ctk.CTkEntry(inner, width=60)
        self.limit_val.insert(0, "50")
        self.limit_val.pack(side="left", padx=10)
        
        self.tree = ttk.Treeview(container, columns=("Check", "STT", "TITLE", "INFO", "STATUS"), show="headings", height=10)
        self.tree.heading("Check", text="☑")
        self.tree.column("Check", width=50, anchor="center")
        
        self.tree.heading("STT", text="STT")
        self.tree.column("STT", width=50, anchor="center")
        
        self.tree.heading("TITLE", text="TIÊU ĐỀ VIDEO")
        self.tree.column("TITLE", width=500, anchor="w")
        
        self.tree.heading("INFO", text="INFO (VIEW/DUR)")
        self.tree.column("INFO", width=150, anchor="center")
        
        self.tree.heading("STATUS", text="TRẠNG THÁI")
        self.tree.column("STATUS", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        
        self.dl_status_lab = ctk.CTkLabel(container, text="Trạng thái: Sẵn sàng", text_color="#8b949e")
        self.dl_status_lab.pack(pady=(10,0))
        
        self.progress_dl = ctk.CTkProgressBar(container, height=12, fg_color="#1c2128", progress_color=CYAN)
        self.progress_dl.set(0)
        self.progress_dl.pack(fill="x", pady=10)
        
        self.btn_dl_main = ctk.CTkButton(container, text="🚀 BẮT ĐẦU TẢI XUỐNG GALAXY", height=60, fg_color=MAGENTA, font=("Arial", 16, "bold"), command=self.run_dl)
        self.btn_dl_main.pack(fill="x")

    def start_scan(self):
        url = self.url_input.get().strip()
        if not url:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập link hoặc nạp file .txt vào ô trống!")
            return
        self.btn_scan.configure(state="disabled", text="⏳ ĐANG QUÉT...")
        self.dl_status_lab.configure(text="Trạng thái: Đang kết nối dữ liệu mạng xã hội...", text_color=CYAN)
        threading.Thread(target=self.scan_thread, args=(url,), daemon=True).start()

    def scan_thread(self, target_input):
        self.after(0, lambda: [self.tree.delete(i) for i in self.tree.get_children()])
        self.video_list.clear()
        try:
            urls_to_scan = []
            if os.path.isfile(target_input):
                with open(target_input, 'r', encoding='utf-8') as f:
                    urls_to_scan = [line.strip() for line in f if line.strip()]
            else:
                urls_to_scan = [target_input]

            try: limit_count = int(self.limit_val.get())
            except: limit_count = 50

            ydl_opts = {
                'extract_flat': True, 
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                count = 0
                for current_url in urls_to_scan:
                    if count >= limit_count: break
                    
                    if "youtube.com/@" in current_url and "/videos" not in current_url and "/shorts" not in current_url:
                        current_url = current_url.rstrip("/") + "/videos"

                    info = ydl.extract_info(current_url, download=False)
                    if not info: continue
                    
                    if 'entries' in info: entries = list(info['entries'])
                    else: entries = [info]

                    for e in entries:
                        if not e: continue
                        if count >= limit_count: break
                        
                        title = e.get('title') or f"Video_{int(time.time())}"
                        views = e.get('view_count', 'N/A')
                        duration = e.get('duration', 'N/A')
                        vinfo = f"{views} Views | {duration}s"
                        url_video = e.get('webpage_url') or e.get('url') or current_url
                        
                        self.after(0, lambda t=title, v=vinfo, u=url_video: self.add_to_tree(t, v, u))
                        count += 1

        except Exception as ex:
            print(f"\n--- LỖI YT-DLP CHI TIẾT ---\n{ex}\n---------------------------\n")
            self.after(0, lambda: messagebox.showerror("Lỗi Quét Dữ Liệu", f"Không thể lấy dữ liệu.\n\nChi tiết lỗi:\n{str(ex)[:150]}..."))
        finally:
            self.after(0, lambda: self.btn_scan.configure(state="normal", text="QUÉT DỮ LIỆU"))
            self.after(0, lambda: self.dl_status_lab.configure(text="Trạng thái: Hoàn tất quét dữ liệu!", text_color=CYAN))

    def add_to_tree(self, title, vinfo, url):
        stt = len(self.video_list) + 1
        tid = self.tree.insert("", "end", values=("☑", stt, title[:100], vinfo, "SẴN SÀNG"))
        self.video_list[tid] = {'url': url}

    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        col = self.tree.identify_column(event.x)
        
        if region == "heading" and col == "#1":
            self.all_selected = not self.all_selected
            mark = "☑" if self.all_selected else "☐"
            for item in self.tree.get_children():
                v = list(self.tree.item(item, "values"))
                v[0] = mark
                self.tree.item(item, values=v)
                
        elif region == "cell" and col == "#1":
            item = self.tree.identify_row(event.y)
            if item:
                v = list(self.tree.item(item, "values"))
                v[0] = "☐" if v[0] == "☑" else "☑"
                self.tree.item(item, values=v)

    def run_dl(self): 
        selected_items = [t for t in self.tree.get_children() if self.tree.item(t, "values")[0] == "☑"]
        if not selected_items:
            messagebox.showwarning("Thông báo", "Anh Jonathan chưa chọn video nào để tải!")
            return
            
        self.update_btn_state(self.btn_dl_main, self.dl_status_lab, self.progress_dl, True, start_text="🚀 BẮT ĐẦU TẢI XUỐNG GALAXY")
        threading.Thread(target=self.dl_worker, args=(selected_items,), daemon=True).start()

    def dl_worker(self, sel_ids):
        save_path = self.dl_path_entry.get().replace("\\", "/")
        mode = self.mode_menu.get()
        res_val = self.res_menu.get()
        if "4K" in res_val:
            res = "2160"
        elif "2K" in res_val:
            res = "1440"
        else:
            res = res_val.replace("p", "")
            
        total_vids = len(sel_ids)

        for idx, item_id in enumerate(sel_ids):
            self.after(0, lambda id=item_id: self.tree.set(id, "STATUS", "⏳ ĐANG TẢI..."))
            try:
                opts = {
                    'outtmpl': f"{save_path}/%(title)s.%(ext)s", 
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                }

                if mode == "Video MP4 + Ảnh JPG":
                    opts['format'] = f'bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                    opts['merge_output_format'] = 'mp4'
                    opts['writethumbnail'] = True
                    opts['postprocessors'] = [
                        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                        {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'}
                    ]
                elif mode == "Chỉ Video MP4":
                    opts['format'] = f'bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                    opts['merge_output_format'] = 'mp4'
                    opts['postprocessors'] = [
                        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}
                    ]
                elif mode == "Chỉ MP3":
                    opts['format'] = 'bestaudio/best'
                    opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
                elif mode == "Chỉ Ảnh JPG":
                    opts['skip_download'] = True
                    opts['writethumbnail'] = True
                    opts['postprocessors'] = [{'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'}]

                with yt_dlp.YoutubeDL(opts) as ydl:
                    target_url = self.video_list[item_id]['url']
                    ydl.download([target_url])
                    
                    try:
                        title_video = self.tree.item(item_id, "values")[2]
                        self.log_to_galaxy_cloud(title=title_video, url=target_url, status="Thành Công")
                    except: pass
                
                self.after(0, lambda id=item_id: self.tree.set(id, "STATUS", "✅ XONG"))
            except Exception as e:
                print(f"\n--- LỖI DOWNLOAD CHI TIẾT ---\n{e}\n---------------------------\n")
                self.after(0, lambda id=item_id: self.tree.set(id, "STATUS", "❌ LỖI"))
                try:
                    title_video = self.tree.item(item_id, "values")[2]
                    target_url = self.video_list[item_id]['url']
                    self.log_to_galaxy_cloud(title=title_video, url=target_url, status="Lỗi")
                except: pass
            
            progress_val = (idx + 1) / total_vids
            self.after(0, lambda v=progress_val: self.progress_dl.set(v))

            if idx < total_vids - 1:
                import random
                delay_time = random.randint(15, 50)
                self.after(0, lambda i=idx, d=delay_time: self.dl_status_lab.configure(
                    text=f"Trạng thái: Đang nghỉ {d}s giả lập người dùng (Đã tải {i+1}/{total_vids})...", 
                    text_color="yellow"
                ))
                time.sleep(delay_time)

        self.after(0, lambda: self.update_btn_state(self.btn_dl_main, self.dl_status_lab, self.progress_dl, False, start_text="🚀 BẮT ĐẦU TẢI XUỐNG GALAXY"))

    def import_txt(self): 
        f = filedialog.askopenfilename()
        if f:
            self.url_input.delete(0, 'end')
            self.url_input.insert(0, f)

if __name__ == "__main__":
    app = JonathanGalaxyMonster()
    app.mainloop()