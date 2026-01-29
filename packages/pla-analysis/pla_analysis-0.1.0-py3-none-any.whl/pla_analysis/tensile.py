import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class TensileOpticalTracker:
    """
    Clase especializada en detectar líneas de extensómetro en una secuencia de imágenes.
    """
    def __init__(self, frames_folder, l0_mm=35.0, a0_mm2=15.0):
        self.frames_folder = frames_folder
        self.l0_mm = l0_mm
        self.a0_mm2 = a0_mm2
        
        # Validar que es una carpeta
        if not os.path.isdir(frames_folder):
            raise ValueError(f"La ruta '{frames_folder}' no es un directorio válido.")

        # Cargar imágenes ordenadas
        self.frames = sorted(
            [f for f in os.listdir(frames_folder) if f.lower().endswith(('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.bmp'))]
        )
        
        if not self.frames:
            raise ValueError(f"No se encontraron imágenes válidas en '{frames_folder}'")

        self.roi = None
        self.px_per_mm = None
        self.desplazamientos = []
        self.binary_threshold = 90

    def seleccionar_roi_interactiva(self):
        """Permite al usuario seleccionar el área de interés."""
        first_frame_path = os.path.join(self.frames_folder, self.frames[0])
        img = cv2.imread(first_frame_path)
        
        if img is None:
            raise ValueError(f"No se pudo leer la imagen: {first_frame_path}")

        print("Selecciona el recuadro que contenga AMBAS líneas")
        try:
            roi = cv2.selectROI("Selecciona la region de interes del extensometro y pulsa ENTER", img, showCrosshair=True)
        finally:
            cv2.destroyAllWindows()
            cv2.waitKey(1) # Asegurar limpieza de eventos
        
        if roi[2] == 0 or roi[3] == 0:
            raise ValueError("Region de interes inválida (ancho o alto es 0).")
            
        self.roi = roi
        return roi

    def _medir_distancia_en_frame(self, img_gray):
        """Calcula distancia y posiciones de líneas."""
        x, y, w, h = self.roi
        crop = img_gray[y:y+h, x:x+w]
        
        # Binarizar (invertido: fondo blanco -> negro, líneas negras -> blancas)
        _, binary = cv2.threshold(crop, self.binary_threshold, 255, cv2.THRESH_BINARY_INV)
        proyeccion_y = np.sum(binary, axis=1)
        
        # Umbral de detección (40% del ancho)
        umbral_pixels = w * 255 * 0.40 
        filas_con_linea = np.where(proyeccion_y > umbral_pixels)[0]
        
        if filas_con_linea.size < 2:
            return None, None, None
            
        top_y_local = filas_con_linea[0]
        bottom_y_local = filas_con_linea[-1]
        
        dist = bottom_y_local - top_y_local
        # Retornar coordenadas globales para dibujar
        return dist, (y + top_y_local), (y + bottom_y_local)

    def _dibujar_dashboard(self, frame_bgr, desplazamiento_actual, frame_idx):
        """Visualización en vivo con GRÁFICA GRANDE."""
        h_video, w_video = frame_bgr.shape[:2]
        ancho_panel = 800 
        panel = np.ones((h_video, ancho_panel, 3), dtype=np.uint8) * 245 
        
        # --- HEADER ---
        altura_header = 120
        cv2.rectangle(panel, (0, 0), (ancho_panel, altura_header), (230, 230, 230), -1)
        cv2.line(panel, (0, altura_header), (ancho_panel, altura_header), (180, 180, 180), 1)

        texto_disp = f"{desplazamiento_actual:.3f} mm" if desplazamiento_actual is not None else "--"
        
        cv2.putText(panel, "Tensile Analysis Live", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 2, cv2.LINE_AA)
        cv2.putText(panel, f"Elongacion: {texto_disp}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 100, 0), 2, cv2.LINE_AA)
        
        # --- GRÁFICA ---
        # Filtramos Nones para pintar solo puntos válidos
        datos_validos = [d for d in self.desplazamientos if d is not None]
        
        if len(datos_validos) > 1:
            margen_x = 50
            margen_y_inf = 50
            y_inicio = altura_header + 30
            h_graf = h_video - y_inicio - margen_y_inf
            w_graf = ancho_panel - 2 * margen_x
            
            min_v = min(datos_validos)
            max_v = max(datos_validos)
            
            if abs(max_v - min_v) < 0.1:
                centro = (max_v + min_v) / 2
                min_v = centro - 0.05
                max_v = centro + 0.05
                
            span = max_v - min_v
            min_v -= span * 0.1
            max_v += span * 0.1
            rango = max_v - min_v
            
            puntos = []
            total = len(self.frames)
            for i, val in enumerate(datos_validos):
                px = int(margen_x + (i / total) * w_graf)
                norm = (val - min_v) / rango
                py = int((y_inicio + h_graf) - (norm * h_graf))
                puntos.append((px, py))
            
            # Ejes
            color_eje = (100,100,100)
            cv2.line(panel, (margen_x, y_inicio), (margen_x, h_video - margen_y_inf), color_eje, 2)
            cv2.line(panel, (margen_x, h_video - margen_y_inf), (ancho_panel - margen_x, h_video - margen_y_inf), color_eje, 2)
            
            # Curva azul gruesa
            if len(puntos) > 1:
                cv2.polylines(panel, [np.array(puntos)], False, (200, 0, 0), 3, cv2.LINE_AA)
                
            if puntos:
                cv2.circle(panel, puntos[-1], 6, (0, 0, 255), -1, cv2.LINE_AA)

        return np.hstack((frame_bgr, panel))

    def procesar(self):
        """Bucle principal."""
        print(f"Procesando {len(self.frames)} frames desde: {self.frames_folder}")
        
        cv2.namedWindow("Tensile Analysis Live", cv2.WINDOW_NORMAL)
        
        x, y, w, h = self.roi
        
        # --- FASE 1: CALIBRACIÓN ---
        temps_calib = []
        for i in range(min(5, len(self.frames))):
            p = os.path.join(self.frames_folder, self.frames[i])
            im = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
            d, _, _ = self._medir_distancia_en_frame(im)
            if d is not None: temps_calib.append(d)
        
        if not temps_calib:
            raise ValueError("No se detectaron líneas al inicio para calibrar.")
            
        dist_inicial_px = np.mean(temps_calib)
        self.px_per_mm = dist_inicial_px / self.l0_mm

        # --- FASE 2: ANÁLISIS ---
        for idx, frame_name in enumerate(self.frames):
            path = os.path.join(self.frames_folder, frame_name)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            frame_vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            
            dist_px, y_top, y_bot = self._medir_distancia_en_frame(img)
            desp_mm = None
            
            cv2.rectangle(frame_vis, (x, y), (x+w, y+h), (0, 255, 0), 1)
            
            if dist_px is not None:
                cv2.line(frame_vis, (x, y_top), (x+w, y_top), (0, 0, 255), 2)
                cv2.line(frame_vis, (x, y_bot), (x+w, y_bot), (0, 0, 255), 2)
                
                longitud_actual_mm = dist_px / self.px_per_mm
                desp_mm = longitud_actual_mm - self.l0_mm
            else:
                if self.desplazamientos:
                    desp_mm = self.desplazamientos[-1]
                cv2.putText(frame_vis, "LOST", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

            self.desplazamientos.append(desp_mm)

            dashboard = self._dibujar_dashboard(frame_vis, desp_mm, idx)
            cv2.imshow("Tensile Analysis Live", dashboard)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Interrumpido por usuario.")
                break
        
        cv2.destroyAllWindows()
        return self.desplazamientos


def analyze(frames_folder, l0_mm=35.0, a0_mm2=15.0):
    """
    Función principal.
    """
    try:
        tracker = TensileOpticalTracker(frames_folder, l0_mm=l0_mm, a0_mm2=a0_mm2)
        tracker.seleccionar_roi_interactiva()
        
        # 1. Procesar (Devuelve una lista con None y floats)
        desplazamientos_lista = tracker.procesar()
        
        # --- CORRECCIÓN DEL ERROR ---
        # Convertimos la lista a un array numpy de floats, cambiando None por np.nan
        # Esto evita el error "integer scalar arrays..." al filtrar
        desplazamientos_arr = np.array(
            [d if d is not None else np.nan for d in desplazamientos_lista], 
            dtype=np.float64
        )
        
        # 2. Calcular Máximo (ignorando NaNs)
        if np.all(np.isnan(desplazamientos_arr)):
            max_disp = 0.0
            print("No se detectó movimiento válido en ningún frame.")
        else:
            max_disp = np.nanmax(desplazamientos_arr)
        
        results = {
            "displacement_mm": desplazamientos_lista,
            "max_displacement": max_disp,
            "parameters": {"l0": l0_mm, "a0": a0_mm2}
        }
        
        # 3. Imprimir resultado
        print(f" RESULTADO FINAL")
        print(f" Desplazamiento Máximo: {max_disp:.4f} mm")
        
        # 4. Gráfica Final
        plt.figure(figsize=(10, 6))
        
        # Usamos el array limpio para graficar
        plt.plot(desplazamientos_arr, color='navy', linewidth=2, label='Extensómetro Óptico')
        plt.axhline(max_disp, color='red', linestyle='--', alpha=0.5, label=f'Max: {max_disp:.2f} mm')
        
        plt.title(f"Gráfica Final (L0={l0_mm}mm)")
        plt.xlabel("Frame")
        plt.ylabel("Elongación [mm]")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        print("Mostrando gráfica final (cierre la ventana para terminar)...")
        plt.show()

        return results

    except Exception as e:
        print(f"Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        return None