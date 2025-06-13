import cv2
import numpy as np
import csv
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import threading
import sys
import math
import matplotlib.pyplot as plt

class ArucoAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Marcadores ArUco")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.aruco_dicts = {
            "4X4": {
                "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
                "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
                "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
                "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000
            },
            "5X5": {
                "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
                "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
                "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
                "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000
            },
            "6X6": {
                "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
                "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
                "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
                "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000
            },
            "7X7": {
                "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
                "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
                "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
                "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000
            }
        }

        self.label = tk.Label(root, text="Seleccione un video para procesar")
        self.label.pack(pady=5)

        self.btn_select_video = tk.Button(root, text="Seleccionar Video", command=self.select_video)
        self.btn_select_video.pack(pady=5)

        self.btn_calibrate = tk.Button(root, text="Calibrar escala (px/mm)", command=self.calibrate_px_per_mm)
        self.btn_calibrate.pack(pady=5)

        self.label_dict = tk.Label(root, text="Seleccione el diccionario ArUco:")
        self.label_dict.pack(pady=5)

        self.dict_combo = ttk.Combobox(root, values=self.get_all_dict_names())
        self.dict_combo.pack(pady=5)
        self.dict_combo.current(0)

        self.btn_start_analysis = tk.Button(root, text="Iniciar Análisis", command=self.start_analysis, state=tk.DISABLED)
        self.btn_start_analysis.pack(pady=5)

        self.btn_stop_analysis = tk.Button(root, text="Detener Análisis", command=self.stop_analysis, state=tk.DISABLED)
        self.btn_stop_analysis.pack(pady=5)

        self.video_label = tk.Label(root)
        self.video_label.pack(padx=10, pady=10)

        self.video_path = None
        self.stop_flag = False
        self.analysis_thread = None
        self.px_per_mm = None

    def on_close(self):
        self.stop_flag = True
        self.root.quit()
        self.root.destroy()
        sys.exit()

    def get_all_dict_names(self):
        names = []
        for group in self.aruco_dicts.values():
            names.extend(group.keys())
        return names

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if self.video_path:
            self.label.config(text=f"Video seleccionado: {os.path.basename(self.video_path)}")
            self.btn_start_analysis.config(state=tk.NORMAL)

    def calibrate_px_per_mm(self):
        if not self.video_path:
            messagebox.showerror("Error", "Primero debe seleccionar un video.")
            return

        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            messagebox.showerror("Error", "No se pudo capturar un fotograma del video.")
            return

        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()

        frame_alto, frame_ancho = frame.shape[:2]
        escala_max = min(pantalla_ancho / frame_ancho, pantalla_alto / frame_alto, 1.0)

        if escala_max < 1.0:
            frame = cv2.resize(frame, (int(frame_ancho * escala_max), int(frame_alto * escala_max)))

        points = []
        clone = frame.copy()
        instructions = "Haz clic en dos puntos con distancia conocida."
        cv2.putText(clone, instructions, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        def click_event(event, x, y, flags, param):
            nonlocal points
            if event == cv2.EVENT_LBUTTONDOWN:
                points.append((x, y))
                cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
                if len(points) == 2:
                    cv2.line(clone, points[0], points[1], (255, 0, 0), 2)
                    cv2.imshow("Calibración", clone)
                    dist_px = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
                    try:
                        real_mm = simpledialog.askfloat("Calibración", "Introduce la distancia real entre los puntos (mm):")
                        if real_mm is None:
                            raise ValueError("Distancia cancelada.")
                        self.px_per_mm = dist_px / real_mm
                        print(f"Calibración completada: {self.px_per_mm:.4f} px/mm")
                        messagebox.showinfo("Calibración", f"Escala: {self.px_per_mm:.4f} px/mm")
                        cv2.setMouseCallback("Calibración", lambda *args : None)
                        cv2.destroyWindow("Calibración")
                    except Exception as e:
                        messagebox.showerror("Error", f"Valor no válido: {e}")
                        cv2.setMouseCallback("Calibración", lambda *args : None)
                        cv2.destroyWindow("Calibración")

        try:
            cv2.imshow("Calibración", clone)
            cv2.setMouseCallback("Calibración", click_event)
            cv2.waitKey(0)
        except Exception as e:
            print("Error al mostrar ventana de calibración:", e)
        finally:
            cv2.setMouseCallback("Calibración", lambda *args : None)
            cv2.destroyAllWindows()

    def start_analysis(self):
        if not self.video_path:
            messagebox.showerror("Error", "Debe seleccionar un video primero")
            return

        self.stop_flag = False
        self.btn_start_analysis.config(state=tk.DISABLED)
        self.btn_stop_analysis.config(state=tk.NORMAL)

        self.analysis_thread = threading.Thread(target=self.analyze_aruco, daemon=True)
        self.analysis_thread.start()

    def stop_analysis(self):
        self.stop_flag = True
        self.btn_stop_analysis.config(state=tk.DISABLED)

    def analyze_aruco(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir el video")
            self.btn_start_analysis.config(state=tk.NORMAL)
            return

        save_folder = os.path.dirname(self.video_path)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        csv_filename = os.path.join(save_folder, f"aruco_tracking_{timestamp}.csv")

        selected_dict_name = self.dict_combo.get()
        aruco_dict = None
        for group in self.aruco_dicts.values():
            if selected_dict_name in group:
                aruco_dict = cv2.aruco.getPredefinedDictionary(group[selected_dict_name])
                break

        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

        with open(csv_filename, "w", newline='') as f:
            csv_writer = csv.writer(f)
            header = ["Tiempo (s)", "ID", "X (mm)" if self.px_per_mm else "X (px)", "Y (mm)" if self.px_per_mm else "Y (px)", "Rotación (°)", "Desplazamiento vertical (mm)"]
            csv_writer.writerow(header)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        datos_por_tiempo = {}
        desplazamientos_relativos = []

        while cap.isOpened():
            if self.stop_flag:
                break
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = detector.detectMarkers(gray)

            current_time = frame_count / fps
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                datos_por_tiempo[current_time] = {}
                for i in range(len(ids)):
                    id_actual = int(ids[i])
                    x, y = np.mean(corners[i][0], axis=0)
                    x1, y1 = corners[i][0][0]
                    x2, y2 = corners[i][0][1]
                    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                    if self.px_per_mm:
                        x_mm = x / self.px_per_mm
                        y_mm = y / self.px_per_mm
                    else:
                        x_mm = x
                        y_mm = y
                    datos_por_tiempo[current_time][id_actual] = (x_mm, y_mm)

                with open(csv_filename, "a", newline='') as f:
                    csv_writer = csv.writer(f)
                    for id_actual, (x_mm, y_mm) in datos_por_tiempo[current_time].items():
                        desplazamiento_actual = ""
                        if 0 in datos_por_tiempo[current_time] and 1 in datos_por_tiempo[current_time]:
                            y0 = datos_por_tiempo[current_time][0][1]
                            y1 = datos_por_tiempo[current_time][1][1]
                            desplazamiento_actual = abs(y1 - y0)
                            if id_actual == 0:
                                desplazamientos_relativos.append((current_time, desplazamiento_actual))
                        csv_writer.writerow([f"{current_time:.4f}", id_actual, f"{x_mm:.2f}", f"{y_mm:.2f}", f"{angle:.2f}", f"{desplazamiento_actual if desplazamiento_actual != '' else ''}"])

            self.display_frame(frame)
            frame_count += 1
        cap.release()

        # Mostrar desplazamiento final
        if desplazamientos_relativos:
            t_inicio, desplazamiento_inicio = desplazamientos_relativos[0]
            t_final, desplazamiento_final = desplazamientos_relativos[-1]
            desplazamiento_neto = desplazamiento_final - desplazamiento_inicio

            # Mostrar en mensaje
            mensaje = (
                f"Desplazamiento vertical relativo entre ID 0 e ID 1:\n\n"
                f"Tiempo inicial: {t_inicio:.4f} s\n"
                f"Desplazamiento inicial: {desplazamiento_inicio:.2f} mm\n\n"
                f"Tiempo final: {t_final:.4f} s\n"
                f"Desplazamiento final: {desplazamiento_final:.2f} mm\n\n"
                f"Desplazamiento neto: {desplazamiento_neto:.2f} mm"
            )
            self.root.after(0, lambda: messagebox.showinfo("Desplazamiento relativo final", mensaje))

            # Imprimir por consola
            print("===== RESULTADOS =====")
            print(f"Tiempo inicial: {t_inicio:.4f} s")
            print(f"Desplazamiento inicial: {desplazamiento_inicio:.2f} mm")
            print(f"Tiempo final: {t_final:.4f} s")
            print(f"Desplazamiento final: {desplazamiento_final:.2f} mm")
            print(f"Desplazamiento neto: {desplazamiento_neto:.2f} mm")

            # Graficar desplazamiento
            tiempos, valores = zip(*desplazamientos_relativos)
            plt.figure(figsize=(8, 4))
            plt.plot(tiempos, valores, marker='o')
            plt.title("Desplazamiento vertical entre ID 0 e ID 1")
            plt.xlabel("Tiempo (s)")
            plt.ylabel("Desplazamiento (mm)")
            plt.grid(True)

            # Anotaciones en la gráfica
            plt.axhline(y=desplazamiento_inicio, color='orange', linestyle='--', label='Inicial')
            plt.axhline(y=desplazamiento_final, color='purple', linestyle='--', label='Final')
            mid = (desplazamiento_inicio + desplazamiento_final) / 2
            x_max = max(tiempos)
            x_annot = x_max * 0.85

            plt.annotate(
                "", 
                xy=(x_annot, desplazamiento_inicio), 
                xytext=(x_annot, desplazamiento_final), 
                arrowprops=dict(arrowstyle='<->', color='blue', lw=2)
            )
            plt.text(x_annot + 0.05, mid, f"{desplazamiento_neto:.2f} mm", color='blue', va='center')

            plt.text(tiempos[0], desplazamiento_inicio, f"Inicio: {desplazamiento_inicio:.2f} mm", color='orange', va='bottom')
            plt.text(tiempos[-1], desplazamiento_final, f"Final: {desplazamiento_final:.2f} mm", color='purple', va='top')

            plt.tight_layout()
            plt.show()

            # Guardar resumen al final del CSV
            with open(csv_filename, "a", newline='') as f:
                f.write("\n")
                f.write(f"# Resumen desplazamiento vertical entre ID 0 e ID 1\n")
                f.write(f"Tiempo inicial (s),{t_inicio:.4f}\n")
                f.write(f"Desplazamiento inicial (mm),{desplazamiento_inicio:.2f}\n")
                f.write(f"Tiempo final (s),{t_final:.4f}\n")
                f.write(f"Desplazamiento final (mm),{desplazamiento_final:.2f}\n")
                f.write(f"Desplazamiento neto (mm),{desplazamiento_neto:.2f}\n")
        else:
            self.root.after(0, lambda: messagebox.showinfo("Desplazamiento relativo final", "No se detectaron ambos marcadores juntos en ningún frame."))

        self.root.after(0, lambda: messagebox.showinfo("Finalizado", f"Análisis completado. Datos guardados en {csv_filename}"))
        self.root.after(0, lambda: self.btn_start_analysis.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.btn_stop_analysis.config(state=tk.DISABLED))


    def display_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (640, 480))
        img = Image.fromarray(frame_resized)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArucoAnalyzerApp(root)
    root.mainloop()
