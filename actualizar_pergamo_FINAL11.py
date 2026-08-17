# -*- coding: utf-8 -*-
"""Script CONSOLIDADO v11 de Pergamo -- Directorio real: catalogo de SLIS/CDC/Lavanderias/CIAM
importable desde CSV (exportado de la hoja "Directorio" del Excel), con selectores en cascada
Subdireccion -> Servicio -> Unidad en Captura y PQRS (reemplaza el texto libre de antes).
Incluye TODO el estado actual del proyecto.
NO toca src/infrastructure/config/firebase.ts (tus credenciales) ni los iconos PNG.
Correlo desde la raiz de tu proyecto: python actualizar_pergamo_FINAL11.py
"""
import os
ARCHIVOS_TEXTO = {
    "package.json": """{
  "name": "pergamo",
  "version": "1.0.0",
  "description": "Aplicación PWA para auditoría de gestión documental y TRD",
  "main": "index.js",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "keywords": [
    "sgil",
    "gestion-documental",
    "react"
  ],
  "author": "Developer_Ecc",
  "license": "ISC",
  "dependencies": {
    "firebase": "^12.16.0",
    "jspdf": "^4.2.1",
    "jspdf-autotable": "^5.0.8",
    "react": "^19.2.7",
    "react-dom": "^19.2.7",
    "xlsx": "^0.18.5"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.3.3",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.3",
    "autoprefixer": "^10.5.4",
    "postcss": "^8.5.23",
    "tailwindcss": "^4.3.3",
    "typescript": "^5.5.4",
    "vite": "^8.1.5",
    "vite-plugin-pwa": "^1.3.0",
    "vite-tsconfig-paths": "^6.1.1"
  }
}
""",
    "public/estanteria-archivo.svg": """<svg width="1400" height="480" viewBox="0 0 1400 480" xmlns="http://www.w3.org/2000/svg">
  <!-- Ilustracion original de estanteria de archivo, generada proceduralmente para Pergamo:
       cada caja tiene cara frontal + cara superior (simula profundidad real) + sombra propia
       proyectada — no es fotografia ni asset de stock. -->
  <defs>
    <linearGradient id="poste0" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0F172A"/></linearGradient><linearGradient id="g60_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g156.66666666666669_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1D4ED8"/><stop offset="100%" stop-color="#1E3A8A"/></linearGradient><linearGradient id="g253.33333333333337_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g60_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g156.66666666666669_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g253.33333333333337_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g60_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1D4ED8"/><stop offset="100%" stop-color="#1E3A8A"/></linearGradient><linearGradient id="g156.66666666666669_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g253.33333333333337_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1D4ED8"/><stop offset="100%" stop-color="#1E3A8A"/></linearGradient><linearGradient id="poste1" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0F172A"/></linearGradient><linearGradient id="g400_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="g496.6666666666667_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g593.3333333333334_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="g400_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="g496.6666666666667_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g593.3333333333334_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g400_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g496.6666666666667_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g593.3333333333334_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="poste2" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0F172A"/></linearGradient><linearGradient id="g740_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g836.6666666666666_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="g933.3333333333333_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g740_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g836.6666666666666_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="g933.3333333333333_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0F766E"/></linearGradient><linearGradient id="g740_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g836.6666666666666_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1D4ED8"/><stop offset="100%" stop-color="#1E3A8A"/></linearGradient><linearGradient id="g933.3333333333333_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="poste3" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0F172A"/></linearGradient><linearGradient id="g1080_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0D9488"/></linearGradient><linearGradient id="g1176.6666666666667_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g1273.3333333333335_70" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g1080_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g1176.6666666666667_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient><linearGradient id="g1273.3333333333335_195" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1D4ED8"/><stop offset="100%" stop-color="#1E3A8A"/></linearGradient><linearGradient id="g1080_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient><linearGradient id="g1176.6666666666667_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1D4ED8"/><stop offset="100%" stop-color="#1E3A8A"/></linearGradient><linearGradient id="g1273.3333333333335_320" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#60A5FA"/><stop offset="100%" stop-color="#2563EB"/></linearGradient>
    <linearGradient id="pisoSombra" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <ellipse cx="700.0" cy="470" rx="537.6" ry="16" fill="url(#pisoSombra)"/>
  <rect x="40" y="40" width="16" height="410" rx="3" fill="url(#poste0)"/><rect x="344" y="40" width="16" height="410" rx="3" fill="url(#poste0)"/><rect x="40" y="40" width="320" height="12" rx="2" fill="url(#poste0)"/><rect x="40" y="188" width="320" height="12" rx="2" fill="url(#poste0)"/><rect x="40" y="313" width="320" height="12" rx="2" fill="url(#poste0)"/><rect x="40" y="438" width="320" height="12" rx="2" fill="url(#poste0)"/><rect x="46" y="450" width="24" height="14" rx="2" fill="#0F172A"/><rect x="330" y="450" width="24" height="14" rx="2" fill="#0F172A"/><g transform="rotate(0.5374384327308758 103.33333333333334 118.0)"><ellipse cx="103.33333333333334" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="60" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g60_70)"/><path d="M60 70 L67.8 61.42 L154.4666666666667 61.42 L146.66666666666669 70 Z" fill="#FFFFFF" opacity="0.75"/><path d="M60 70 L67.8 61.42 L154.4666666666667 61.42 L146.66666666666669 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="70.4" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="70.4" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.1811213676478245 200.00000000000003 118.0)"><ellipse cx="200.00000000000003" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="156.66666666666669" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g156.66666666666669_70)"/><path d="M156.66666666666669 70 L164.4666666666667 61.42 L251.13333333333338 61.42 L243.33333333333337 70 Z" fill="#1D4ED8" opacity="0.75"/><path d="M156.66666666666669 70 L164.4666666666667 61.42 L251.13333333333338 61.42 L243.33333333333337 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="167.0666666666667" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="167.0666666666667" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.3855291503895699 296.6666666666667 118.0)"><ellipse cx="296.6666666666667" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="253.33333333333337" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g253.33333333333337_70)"/><path d="M253.33333333333337 70 L261.1333333333334 61.42 L347.80000000000007 61.42 L340.00000000000006 70 Z" fill="#60A5FA" opacity="0.75"/><path d="M253.33333333333337 70 L261.1333333333334 61.42 L347.80000000000007 61.42 L340.00000000000006 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="263.73333333333335" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="263.73333333333335" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.16117329970489735 103.33333333333334 243.0)"><ellipse cx="103.33333333333334" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="60" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g60_195)"/><path d="M60 195 L67.8 186.42 L154.4666666666667 186.42 L146.66666666666669 195 Z" fill="#60A5FA" opacity="0.75"/><path d="M60 195 L67.8 186.42 L154.4666666666667 186.42 L146.66666666666669 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="70.4" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="70.4" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.4916448757717228 200.00000000000003 243.0)"><ellipse cx="200.00000000000003" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="156.66666666666669" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g156.66666666666669_195)"/><path d="M156.66666666666669 195 L164.4666666666667 186.42 L251.13333333333338 186.42 L243.33333333333337 195 Z" fill="#60A5FA" opacity="0.75"/><path d="M156.66666666666669 195 L164.4666666666667 186.42 L251.13333333333338 186.42 L243.33333333333337 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="167.0666666666667" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="167.0666666666667" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.5550052098696181 296.6666666666667 243.0)"><ellipse cx="296.6666666666667" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="253.33333333333337" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g253.33333333333337_195)"/><path d="M253.33333333333337 195 L261.1333333333334 186.42 L347.80000000000007 186.42 L340.00000000000006 195 Z" fill="#5EEAD4" opacity="0.75"/><path d="M253.33333333333337 195 L261.1333333333334 186.42 L347.80000000000007 186.42 L340.00000000000006 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="263.73333333333335" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="263.73333333333335" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.09819341835508866 103.33333333333334 368.0)"><ellipse cx="103.33333333333334" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="60" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g60_320)"/><path d="M60 320 L67.8 311.42 L154.4666666666667 311.42 L146.66666666666669 320 Z" fill="#1D4ED8" opacity="0.75"/><path d="M60 320 L67.8 311.42 L154.4666666666667 311.42 L146.66666666666669 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="70.4" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="70.4" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.49114438398736193 200.00000000000003 368.0)"><ellipse cx="200.00000000000003" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="156.66666666666669" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g156.66666666666669_320)"/><path d="M156.66666666666669 320 L164.4666666666667 311.42 L251.13333333333338 311.42 L243.33333333333337 320 Z" fill="#5EEAD4" opacity="0.75"/><path d="M156.66666666666669 320 L164.4666666666667 311.42 L251.13333333333338 311.42 L243.33333333333337 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="167.0666666666667" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="167.0666666666667" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.529067392705213 296.6666666666667 368.0)"><ellipse cx="296.6666666666667" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="253.33333333333337" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g253.33333333333337_320)"/><path d="M253.33333333333337 320 L261.1333333333334 311.42 L347.80000000000007 311.42 L340.00000000000006 320 Z" fill="#1D4ED8" opacity="0.75"/><path d="M253.33333333333337 320 L261.1333333333334 311.42 L347.80000000000007 311.42 L340.00000000000006 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="263.73333333333335" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="263.73333333333335" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><rect x="380" y="40" width="16" height="410" rx="3" fill="url(#poste1)"/><rect x="684" y="40" width="16" height="410" rx="3" fill="url(#poste1)"/><rect x="380" y="40" width="320" height="12" rx="2" fill="url(#poste1)"/><rect x="380" y="188" width="320" height="12" rx="2" fill="url(#poste1)"/><rect x="380" y="313" width="320" height="12" rx="2" fill="url(#poste1)"/><rect x="380" y="438" width="320" height="12" rx="2" fill="url(#poste1)"/><rect x="386" y="450" width="24" height="14" rx="2" fill="#0F172A"/><rect x="670" y="450" width="24" height="14" rx="2" fill="#0F172A"/><g transform="rotate(-0.4514376466204253 443.3333333333333 118.0)"><ellipse cx="443.3333333333333" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="400" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g400_70)"/><path d="M400 70 L407.8 61.42 L494.4666666666667 61.42 L486.6666666666667 70 Z" fill="#2DD4BF" opacity="0.75"/><path d="M400 70 L407.8 61.42 L494.4666666666667 61.42 L486.6666666666667 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="410.4" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="410.4" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.15675109887808447 540.0 118.0)"><ellipse cx="540.0" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="496.6666666666667" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g496.6666666666667_70)"/><path d="M496.6666666666667 70 L504.4666666666667 61.42 L591.1333333333333 61.42 L583.3333333333334 70 Z" fill="#5EEAD4" opacity="0.75"/><path d="M496.6666666666667 70 L504.4666666666667 61.42 L591.1333333333333 61.42 L583.3333333333334 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="507.06666666666666" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="507.06666666666666" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.5372507309484068 636.6666666666667 118.0)"><ellipse cx="636.6666666666667" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="593.3333333333334" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g593.3333333333334_70)"/><path d="M593.3333333333334 70 L601.1333333333333 61.42 L687.8 61.42 L680.0 70 Z" fill="#2DD4BF" opacity="0.75"/><path d="M593.3333333333334 70 L601.1333333333333 61.42 L687.8 61.42 L680.0 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="603.7333333333333" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="603.7333333333333" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.10264970716846411 443.3333333333333 243.0)"><ellipse cx="443.3333333333333" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="400" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g400_195)"/><path d="M400 195 L407.8 186.42 L494.4666666666667 186.42 L486.6666666666667 195 Z" fill="#2DD4BF" opacity="0.75"/><path d="M400 195 L407.8 186.42 L494.4666666666667 186.42 L486.6666666666667 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="410.4" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="410.4" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.5715061267115041 540.0 243.0)"><ellipse cx="540.0" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="496.6666666666667" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g496.6666666666667_195)"/><path d="M496.6666666666667 195 L504.4666666666667 186.42 L591.1333333333333 186.42 L583.3333333333334 195 Z" fill="#60A5FA" opacity="0.75"/><path d="M496.6666666666667 195 L504.4666666666667 186.42 L591.1333333333333 186.42 L583.3333333333334 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="507.06666666666666" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="507.06666666666666" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.06799787752451114 636.6666666666667 243.0)"><ellipse cx="636.6666666666667" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="593.3333333333334" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g593.3333333333334_195)"/><path d="M593.3333333333334 195 L601.1333333333333 186.42 L687.8 186.42 L680.0 195 Z" fill="#60A5FA" opacity="0.75"/><path d="M593.3333333333334 195 L601.1333333333333 186.42 L687.8 186.42 L680.0 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="603.7333333333333" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="603.7333333333333" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.25246885640198846 443.3333333333333 368.0)"><ellipse cx="443.3333333333333" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="400" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g400_320)"/><path d="M400 320 L407.8 311.42 L494.4666666666667 311.42 L486.6666666666667 320 Z" fill="#5EEAD4" opacity="0.75"/><path d="M400 320 L407.8 311.42 L494.4666666666667 311.42 L486.6666666666667 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="410.4" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="410.4" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.048823062638570947 540.0 368.0)"><ellipse cx="540.0" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="496.6666666666667" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g496.6666666666667_320)"/><path d="M496.6666666666667 320 L504.4666666666667 311.42 L591.1333333333333 311.42 L583.3333333333334 320 Z" fill="#5EEAD4" opacity="0.75"/><path d="M496.6666666666667 320 L504.4666666666667 311.42 L591.1333333333333 311.42 L583.3333333333334 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="507.06666666666666" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="507.06666666666666" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.22982181107767874 636.6666666666667 368.0)"><ellipse cx="636.6666666666667" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="593.3333333333334" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g593.3333333333334_320)"/><path d="M593.3333333333334 320 L601.1333333333333 311.42 L687.8 311.42 L680.0 320 Z" fill="#2DD4BF" opacity="0.75"/><path d="M593.3333333333334 320 L601.1333333333333 311.42 L687.8 311.42 L680.0 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="603.7333333333333" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="603.7333333333333" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><rect x="720" y="40" width="16" height="410" rx="3" fill="url(#poste2)"/><rect x="1024" y="40" width="16" height="410" rx="3" fill="url(#poste2)"/><rect x="720" y="40" width="320" height="12" rx="2" fill="url(#poste2)"/><rect x="720" y="188" width="320" height="12" rx="2" fill="url(#poste2)"/><rect x="720" y="313" width="320" height="12" rx="2" fill="url(#poste2)"/><rect x="720" y="438" width="320" height="12" rx="2" fill="url(#poste2)"/><rect x="726" y="450" width="24" height="14" rx="2" fill="#0F172A"/><rect x="1010" y="450" width="24" height="14" rx="2" fill="#0F172A"/><g transform="rotate(-0.47633314506769037 783.3333333333334 118.0)"><ellipse cx="783.3333333333334" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="740" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g740_70)"/><path d="M740 70 L747.8 61.42 L834.4666666666666 61.42 L826.6666666666666 70 Z" fill="#5EEAD4" opacity="0.75"/><path d="M740 70 L747.8 61.42 L834.4666666666666 61.42 L826.6666666666666 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="750.4" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="750.4" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.16669616271142085 880.0 118.0)"><ellipse cx="880.0" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="836.6666666666666" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g836.6666666666666_70)"/><path d="M836.6666666666666 70 L844.4666666666666 61.42 L931.1333333333332 61.42 L923.3333333333333 70 Z" fill="#2DD4BF" opacity="0.75"/><path d="M836.6666666666666 70 L844.4666666666666 61.42 L931.1333333333332 61.42 L923.3333333333333 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="847.0666666666666" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="847.0666666666666" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.48308330880631994 976.6666666666666 118.0)"><ellipse cx="976.6666666666666" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="933.3333333333333" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g933.3333333333333_70)"/><path d="M933.3333333333333 70 L941.1333333333332 61.42 L1027.8 61.42 L1019.9999999999999 70 Z" fill="#FFFFFF" opacity="0.75"/><path d="M933.3333333333333 70 L941.1333333333332 61.42 L1027.8 61.42 L1019.9999999999999 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="943.7333333333332" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="943.7333333333332" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.07724195176006399 783.3333333333334 243.0)"><ellipse cx="783.3333333333334" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="740" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g740_195)"/><path d="M740 195 L747.8 186.42 L834.4666666666666 186.42 L826.6666666666666 195 Z" fill="#60A5FA" opacity="0.75"/><path d="M740 195 L747.8 186.42 L834.4666666666666 186.42 L826.6666666666666 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="750.4" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="750.4" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.3528495446168082 880.0 243.0)"><ellipse cx="880.0" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="836.6666666666666" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g836.6666666666666_195)"/><path d="M836.6666666666666 195 L844.4666666666666 186.42 L931.1333333333332 186.42 L923.3333333333333 195 Z" fill="#2DD4BF" opacity="0.75"/><path d="M836.6666666666666 195 L844.4666666666666 186.42 L931.1333333333332 186.42 L923.3333333333333 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="847.0666666666666" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="847.0666666666666" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.0868892331967166 976.6666666666666 243.0)"><ellipse cx="976.6666666666666" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="933.3333333333333" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g933.3333333333333_195)"/><path d="M933.3333333333333 195 L941.1333333333332 186.42 L1027.8 186.42 L1019.9999999999999 195 Z" fill="#2DD4BF" opacity="0.75"/><path d="M933.3333333333333 195 L941.1333333333332 186.42 L1027.8 186.42 L1019.9999999999999 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="943.7333333333332" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="943.7333333333332" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.04127776099239122 783.3333333333334 368.0)"><ellipse cx="783.3333333333334" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="740" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g740_320)"/><path d="M740 320 L747.8 311.42 L834.4666666666666 311.42 L826.6666666666666 320 Z" fill="#FFFFFF" opacity="0.75"/><path d="M740 320 L747.8 311.42 L834.4666666666666 311.42 L826.6666666666666 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="750.4" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="750.4" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.16610117286652037 880.0 368.0)"><ellipse cx="880.0" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="836.6666666666666" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g836.6666666666666_320)"/><path d="M836.6666666666666 320 L844.4666666666666 311.42 L931.1333333333332 311.42 L923.3333333333333 320 Z" fill="#1D4ED8" opacity="0.75"/><path d="M836.6666666666666 320 L844.4666666666666 311.42 L931.1333333333332 311.42 L923.3333333333333 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="847.0666666666666" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="847.0666666666666" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.35325537782698935 976.6666666666666 368.0)"><ellipse cx="976.6666666666666" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="933.3333333333333" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g933.3333333333333_320)"/><path d="M933.3333333333333 320 L941.1333333333332 311.42 L1027.8 311.42 L1019.9999999999999 320 Z" fill="#5EEAD4" opacity="0.75"/><path d="M933.3333333333333 320 L941.1333333333332 311.42 L1027.8 311.42 L1019.9999999999999 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="943.7333333333332" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="943.7333333333332" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><rect x="1060" y="40" width="16" height="410" rx="3" fill="url(#poste3)"/><rect x="1364" y="40" width="16" height="410" rx="3" fill="url(#poste3)"/><rect x="1060" y="40" width="320" height="12" rx="2" fill="url(#poste3)"/><rect x="1060" y="188" width="320" height="12" rx="2" fill="url(#poste3)"/><rect x="1060" y="313" width="320" height="12" rx="2" fill="url(#poste3)"/><rect x="1060" y="438" width="320" height="12" rx="2" fill="url(#poste3)"/><rect x="1066" y="450" width="24" height="14" rx="2" fill="#0F172A"/><rect x="1350" y="450" width="24" height="14" rx="2" fill="#0F172A"/><g transform="rotate(-0.5017739870450761 1123.3333333333333 118.0)"><ellipse cx="1123.3333333333333" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1080" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g1080_70)"/><path d="M1080 70 L1087.8 61.42 L1174.4666666666667 61.42 L1166.6666666666667 70 Z" fill="#5EEAD4" opacity="0.75"/><path d="M1080 70 L1087.8 61.42 L1174.4666666666667 61.42 L1166.6666666666667 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1090.4" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1090.4" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.030235804573741754 1220.0 118.0)"><ellipse cx="1220.0" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1176.6666666666667" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g1176.6666666666667_70)"/><path d="M1176.6666666666667 70 L1184.4666666666667 61.42 L1271.1333333333334 61.42 L1263.3333333333335 70 Z" fill="#FFFFFF" opacity="0.75"/><path d="M1176.6666666666667 70 L1184.4666666666667 61.42 L1271.1333333333334 61.42 L1263.3333333333335 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1187.0666666666668" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1187.0666666666668" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.2753343473270611 1316.6666666666667 118.0)"><ellipse cx="1316.6666666666667" cy="172" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1273.3333333333335" y="70" width="86.66666666666667" height="96" rx="4" fill="url(#g1273.3333333333335_70)"/><path d="M1273.3333333333335 70 L1281.1333333333334 61.42 L1367.8000000000002 61.42 L1360.0000000000002 70 Z" fill="#FFFFFF" opacity="0.75"/><path d="M1273.3333333333335 70 L1281.1333333333334 61.42 L1367.8000000000002 61.42 L1360.0000000000002 70" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1283.7333333333336" y="85.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1283.7333333333336" y="100.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.13075082284368433 1123.3333333333333 243.0)"><ellipse cx="1123.3333333333333" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1080" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g1080_195)"/><path d="M1080 195 L1087.8 186.42 L1174.4666666666667 186.42 L1166.6666666666667 195 Z" fill="#FFFFFF" opacity="0.75"/><path d="M1080 195 L1087.8 186.42 L1174.4666666666667 186.42 L1166.6666666666667 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1090.4" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1090.4" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.45832106609404544 1220.0 243.0)"><ellipse cx="1220.0" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1176.6666666666667" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g1176.6666666666667_195)"/><path d="M1176.6666666666667 195 L1184.4666666666667 186.42 L1271.1333333333334 186.42 L1263.3333333333335 195 Z" fill="#60A5FA" opacity="0.75"/><path d="M1176.6666666666667 195 L1184.4666666666667 186.42 L1271.1333333333334 186.42 L1263.3333333333335 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1187.0666666666668" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1187.0666666666668" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.4020454756277121 1316.6666666666667 243.0)"><ellipse cx="1316.6666666666667" cy="297" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1273.3333333333335" y="195" width="86.66666666666667" height="96" rx="4" fill="url(#g1273.3333333333335_195)"/><path d="M1273.3333333333335 195 L1281.1333333333334 186.42 L1367.8000000000002 186.42 L1360.0000000000002 195 Z" fill="#1D4ED8" opacity="0.75"/><path d="M1273.3333333333335 195 L1281.1333333333334 186.42 L1367.8000000000002 186.42 L1360.0000000000002 195" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1283.7333333333336" y="210.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1283.7333333333336" y="225.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.41761855840739426 1123.3333333333333 368.0)"><ellipse cx="1123.3333333333333" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1080" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g1080_320)"/><path d="M1080 320 L1087.8 311.42 L1174.4666666666667 311.42 L1166.6666666666667 320 Z" fill="#FFFFFF" opacity="0.75"/><path d="M1080 320 L1087.8 311.42 L1174.4666666666667 311.42 L1166.6666666666667 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1090.4" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1090.4" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(-0.09396197462790679 1220.0 368.0)"><ellipse cx="1220.0" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1176.6666666666667" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g1176.6666666666667_320)"/><path d="M1176.6666666666667 320 L1184.4666666666667 311.42 L1271.1333333333334 311.42 L1263.3333333333335 320 Z" fill="#1D4ED8" opacity="0.75"/><path d="M1176.6666666666667 320 L1184.4666666666667 311.42 L1271.1333333333334 311.42 L1263.3333333333335 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1187.0666666666668" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1187.0666666666668" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g><g transform="rotate(0.31748503945537576 1316.6666666666667 368.0)"><ellipse cx="1316.6666666666667" cy="422" rx="39.86666666666667" ry="5" fill="#0F172A" opacity="0.10"/><rect x="1273.3333333333335" y="320" width="86.66666666666667" height="96" rx="4" fill="url(#g1273.3333333333335_320)"/><path d="M1273.3333333333335 320 L1281.1333333333334 311.42 L1367.8000000000002 311.42 L1360.0000000000002 320 Z" fill="#60A5FA" opacity="0.75"/><path d="M1273.3333333333335 320 L1281.1333333333334 311.42 L1367.8000000000002 311.42 L1360.0000000000002 320" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5"/><rect x="1283.7333333333336" y="335.36" width="60.666666666666664" height="10.56" rx="2" fill="#FFFFFF" opacity="0.85"/><rect x="1283.7333333333336" y="350.72" width="36.4" height="5.76" rx="1.5" fill="#FFFFFF" opacity="0.45"/></g>
</svg>""",
    "public/patron-archivo.svg": """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Patron original alusivo a gestion documental: cajas de archivo, carpetas y folios,
       estilo de linea, disenado para este proyecto (no es una imagen de stock). -->
  <g fill="none" stroke="#166534" stroke-width="1.4" stroke-opacity="0.10">
    <!-- Caja de archivo (esquina superior izquierda) -->
    <rect x="14" y="18" width="46" height="32" rx="2"/>
    <rect x="14" y="18" width="46" height="9" rx="2"/>
    <line x1="30" y1="18" x2="30" y2="9"/>
    <line x1="44" y1="18" x2="44" y2="9"/>
    <line x1="30" y1="9" x2="44" y2="9"/>

    <!-- Carpeta con pestana -->
    <path d="M110 24 h34 v28 h-34 z"/>
    <path d="M110 24 l6 -6 h14 l4 6"/>

    <!-- Folios apilados -->
    <rect x="150" y="110" width="30" height="38" rx="1.5"/>
    <rect x="146" y="106" width="30" height="38" rx="1.5"/>
    <rect x="142" y="102" width="30" height="38" rx="1.5"/>
    <line x1="148" y1="112" x2="166" y2="112"/>
    <line x1="148" y1="118" x2="166" y2="118"/>
    <line x1="148" y1="124" x2="162" y2="124"/>

    <!-- Segunda caja de archivo, mas abajo -->
    <rect x="24" y="132" width="42" height="30" rx="2"/>
    <rect x="24" y="132" width="42" height="8" rx="2"/>
    <line x1="38" y1="132" x2="38" y2="124"/>
    <line x1="52" y1="132" x2="52" y2="124"/>
    <line x1="38" y1="124" x2="52" y2="124"/>

    <!-- Sello / estampilla circular, alude al "Semaforo" y trazabilidad -->
    <circle cx="176" cy="60" r="12"/>
    <circle cx="176" cy="60" r="7"/>
  </g>
</svg>
""",
    "src/application/builders/RegistroPeriodoBuilder.ts": """// Patron Builder: arma un RegistroPeriodo paso a paso, con valores por defecto sensatos para
// cada sub-objeto (tareas, transferencia, diagnostico), en vez de que cada pantalla tenga que
// saber construir a mano toda la forma del objeto. Sirve tanto para el formulario de captura
// como para pruebas/semillas de datos.
import type {
  RegistroPeriodo,
  PeriodoTRD,
  TareasCantidad,
  Transferencia,
  DiagnosticoRiesgo,
  TipoAlmacenamiento,
} from "../../domain/entities/RegistroPeriodo";

type RegistroBorrador = Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">;

export class RegistroPeriodoBuilder {
  private borrador: RegistroBorrador = {
    unidadOperativaId: "",
    periodo: "Fondo Acumulado (FDA)",
    totalCajas: 0,
    tareas: {
      fuid: 0, eliminacion: null, clasificacion: 0, ordenacion: 0,
      foliacion: 0, hojaControl: 0, rotulacion: 0,
    },
    transferencia: {
      correoSAF: false, aprobacionSAF: false, trasladoArchivoCentral: false, cajasTrasladadas: 0,
    },
    diagnostico: {
      tipoAlmacenamiento: null,
      riesgoHumedad: null, riesgoRoedores: null, riesgoSobreapilamiento: null, riesgoFiltraciones: null,
      cajasSobreapiladas: 0, metrosEspacioAjenoInvadido: 0,
    },
  };

  paraUnidad(unidadOperativaId: string): this {
    this.borrador.unidadOperativaId = unidadOperativaId;
    return this;
  }

  enPeriodo(periodo: PeriodoTRD): this {
    this.borrador.periodo = periodo;
    return this;
  }

  conTotalCajas(totalCajas: number): this {
    this.borrador.totalCajas = totalCajas;
    return this;
  }

  conTareas(tareas: Partial<TareasCantidad>): this {
    this.borrador.tareas = { ...this.borrador.tareas, ...tareas };
    return this;
  }

  conTransferencia(transferencia: Partial<Transferencia>): this {
    this.borrador.transferencia = { ...this.borrador.transferencia, ...transferencia };
    return this;
  }

  conDiagnostico(diagnostico: Partial<DiagnosticoRiesgo>): this {
    this.borrador.diagnostico = { ...this.borrador.diagnostico, ...diagnostico };
    return this;
  }

  conTipoAlmacenamiento(tipo: TipoAlmacenamiento): this {
    this.borrador.diagnostico.tipoAlmacenamiento = tipo;
    return this;
  }

  conEncargado(encargado: string): this {
    this.borrador.encargado = encargado;
    return this;
  }

  conFechaVisita(fechaISO: string): this {
    this.borrador.fechaVisita = fechaISO;
    return this;
  }

  conObservaciones(observaciones: string): this {
    this.borrador.observaciones = observaciones;
    return this;
  }

  /** Valida lo mínimo indispensable antes de entregar el objeto -- espejo de las reglas del
   *  caso de uso RegistrarAvancePeriodo, para fallar rápido si algo llega incompleto. */
  build(): RegistroBorrador {
    if (!this.borrador.unidadOperativaId) {
      throw new Error("RegistroPeriodoBuilder: falta especificar la unidad operativa (.paraUnidad()).");
    }
    if (this.borrador.totalCajas <= 0) {
      throw new Error("RegistroPeriodoBuilder: totalCajas debe ser mayor a 0 (.conTotalCajas()).");
    }
    return { ...this.borrador };
  }
}
""",
    "src/application/services/CalcularResumenDashboard.ts": """// Calcula el resumen del Tablero del lado del cliente -- reutiliza EXACTAMENTE las mismas
// funciones de dominio que ya validamos (calcularAvanceTotal, semaforo, cajasVigentes,
// avanceOrganizacionPQRS) en vez de reinventar la formula aqui. Si algun dia se agrega una
// Cloud Function para pre-calcular esto en el servidor, la logica de negocio no cambia -- solo
// cambia QUIEN la ejecuta.
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { calcularAvanceTotal, cajasVigentes, semaforo, nivelRiesgo } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import { avanceOrganizacionPQRS, cajasVigentesPQRS } from "../../domain/entities/PQRS";
import type { ResumenDashboard } from "../../domain/repositories/IRegistroPeriodoRepository";

const TAREAS_ORDEN: Array<{ key: keyof RegistroPeriodo["tareas"]; label: string }> = [
  { key: "fuid", label: "FUID" },
  { key: "eliminacion", label: "Eliminación" },
  { key: "clasificacion", label: "Clasificación" },
  { key: "ordenacion", label: "Ordenación" },
  { key: "foliacion", label: "Foliación" },
  { key: "hojaControl", label: "Hoja de Control" },
  { key: "rotulacion", label: "Rotulación" },
];

export function calcularResumenDashboard(registros: RegistroPeriodo[], pqrs: PQRS[]): ResumenDashboard {
  const cajasVigentesEnSitio = registros.reduce((acc, r) => acc + cajasVigentes(r), 0);
  const totalCajasHistorico = registros.reduce((acc, r) => acc + r.totalCajas, 0);
  const avances = registros.map((r) => calcularAvanceTotal(r));
  const avancePromedioGlobal = avances.length ? avances.reduce((a, b) => a + b, 0) / avances.length : 0;
  const unidadesOperativas = new Set(registros.map((r) => r.unidadOperativaId)).size;

  const cajasEliminacionHistorico = registros.reduce((acc, r) => acc + (r.tareas.eliminacion ?? 0), 0);
  const hoy = new Date(); const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1).toISOString();
  const cajasEliminacionEstePeriodo = registros
    .filter((r) => r.actualizadoEn >= inicioMes)
    .reduce((acc, r) => acc + (r.tareas.eliminacion ?? 0), 0);

  const unidadesEnRiesgoAlto = new Set(
    registros.filter((r) => nivelRiesgo(r.diagnostico) === "rojo").map((r) => r.unidadOperativaId)
  ).size;

  const cajasSobreapiladas = registros.reduce((acc, r) => acc + (r.diagnostico.cajasSobreapiladas || 0), 0)
    + pqrs.reduce((acc, p) => acc + 0, 0); // PQRS no tiene diagnostico de riesgo propio, solo RegistroPeriodo
  const metrosEspacioAjenoInvadido = registros.reduce((acc, r) => acc + (r.diagnostico.metrosEspacioAjenoInvadido || 0), 0);

  // Por Dependencia/Servicio -- agrupado sobre el id de unidad (no tenemos Directorio con
  // Dependencia/Servicio real todavia; se usa el identificador de la unidad como agrupador
  // temporal hasta que se construya esa vinculacion, ver nota en README).
  const grupos = new Map<string, RegistroPeriodo[]>();
  for (const r of registros) {
    const clave = r.unidadOperativaId;
    grupos.set(clave, [...(grupos.get(clave) ?? []), r]);
  }
  const porDependenciaServicio = Array.from(grupos.entries()).map(([unidad, regs]) => ({
    dependencia: unidad, servicio: "",
    totalCajas: regs.reduce((acc, r) => acc + cajasVigentes(r), 0),
    avancePromedio: regs.reduce((acc, r) => acc + calcularAvanceTotal(r), 0) / regs.length,
  }));

  const porTarea = TAREAS_ORDEN.map(({ key, label }) => {
    const valores = registros
      .map((r) => {
        const cant = r.tareas[key];
        if (cant === null || cant === undefined) return null;
        return r.totalCajas > 0 ? cant / r.totalCajas : 0;
      })
      .filter((v): v is number => v !== null);
    return { tarea: label, avancePromedio: valores.length ? valores.reduce((a, b) => a + b, 0) / valores.length : 0 };
  });

  const periodos = new Map<string, RegistroPeriodo[]>();
  for (const r of registros) periodos.set(r.periodo, [...(periodos.get(r.periodo) ?? []), r]);
  const porPeriodo = Array.from(periodos.entries()).map(([periodo, regs]) => ({
    periodo,
    totalCajas: regs.reduce((acc, r) => acc + cajasVigentes(r), 0),
    avancePromedio: regs.reduce((acc, r) => acc + calcularAvanceTotal(r), 0) / regs.length,
  }));

  return {
    cajasVigentesEnSitio, totalCajasHistorico, avancePromedioGlobal, unidadesOperativas,
    cajasEliminacionHistorico, cajasEliminacionEstePeriodo, unidadesEnRiesgoAlto,
    cajasSobreapiladas, metrosEspacioAjenoInvadido,
    porDependenciaServicio, porTarea, porPeriodo,
    // Sobreapilamiento por Subdireccion: pendiente de un Directorio real que vincule
    // unidadOperativaId -> subdireccionLocal (ver README, "Proximo paso").
    sobreapilamientoPorSubdireccion: [],
    actualizadoEn: new Date().toISOString(),
  };
}

export { semaforo };
""",
    "src/application/useCases/RegistrarAvancePeriodo.ts": """import type { IRegistroPeriodoRepository } from "../../domain/repositories/IRegistroPeriodoRepository";
import type {
  RegistroPeriodo,
  TareasCantidad,
  Transferencia,
  DiagnosticoRiesgo,
} from "../../domain/entities/RegistroPeriodo";

export interface RegistrarAvanceInput {
  unidadOperativaId: string;
  periodo: RegistroPeriodo["periodo"];
  totalCajas: number;
  tareas: TareasCantidad;
  transferencia: Transferencia;
  diagnostico: DiagnosticoRiesgo;
  encargado?: string;
  fechaVisita?: string;
  observaciones?: string;
}

export class ValidacionError extends Error {}

// Caso de uso: orquesta la regla de negocio + el repositorio. No sabe que existe Firebase.
export class RegistrarAvancePeriodo {
  constructor(private readonly repo: IRegistroPeriodoRepository) {}

  async ejecutar(input: RegistrarAvanceInput): Promise<RegistroPeriodo> {
    if (input.totalCajas <= 0) {
      throw new ValidacionError("Total Cajas (Meta) debe ser mayor a 0.");
    }
    // Espejo de la regla que vive en las Security Rules de Firestore (defensa en profundidad):
    // ninguna tarea puede tener mas cajas que el total del periodo. Eliminacion puede ser null
    // ("N/A" -- ese periodo no tiene nada que eliminar), en ese caso no se valida.
    for (const [tarea, cantidad] of Object.entries(input.tareas)) {
      if (cantidad === null || cantidad === undefined) continue; // N/A valido, no es un error
      if (cantidad < 0) throw new ValidacionError(`${tarea}: la cantidad no puede ser negativa.`);
      if (cantidad > input.totalCajas) {
        throw new ValidacionError(
          `${tarea}: ${cantidad} cajas supera el Total Cajas (Meta) de ${input.totalCajas}. Revisa el dato.`
        );
      }
    }
    if (input.transferencia.cajasTrasladadas > input.totalCajas) {
      throw new ValidacionError("Cajas Trasladadas no puede superar el Total Cajas (Meta).");
    }
    return this.repo.guardar(input);
  }
}
""",
    "src/application/useCases/RegistrarPQRS.ts": """import type { IPQRSRepository } from "../../domain/repositories/IPQRSRepository";
import type { PQRS, TrasladoPQRS } from "../../domain/entities/PQRS";
import { puedeIniciarTraslado } from "../../domain/entities/PQRS";
import type { TareasCantidad } from "../../domain/entities/RegistroPeriodo";

export interface RegistrarPQRSInput {
  unidadOperativaId: string;
  totalCajas: number;
  tareas: TareasCantidad;
  traslado: TrasladoPQRS;
  encargado?: string;
  fechaVisita?: string;
  observaciones?: string;
}

export class ValidacionPQRSError extends Error {}

export class RegistrarPQRS {
  constructor(private readonly repo: IPQRSRepository) {}

  async ejecutar(input: RegistrarPQRSInput): Promise<PQRS> {
    if (input.totalCajas <= 0) {
      throw new ValidacionPQRSError("El total de cajas debe ser mayor a 0.");
    }
    for (const [tarea, cantidad] of Object.entries(input.tareas)) {
      if (cantidad === null || cantidad === undefined) continue;
      if (cantidad < 0) throw new ValidacionPQRSError(`${tarea}: la cantidad no puede ser negativa.`);
      if (cantidad > input.totalCajas) {
        throw new ValidacionPQRSError(`${tarea}: ${cantidad} cajas supera el total de ${input.totalCajas}.`);
      }
    }
    // Regla de negocio central de PQRS: no se puede notificar a la Subsecretaria de Gestion
    // Institucional ni marcar traslado sobre PQRS que aun no completo su organizacion.
    if (
      (input.traslado.correoEnviado || input.traslado.trasladado) &&
      !puedeIniciarTraslado({ totalCajas: input.totalCajas, tareas: input.tareas })
    ) {
      throw new ValidacionPQRSError(
        "No se puede notificar ni trasladar PQRS cuya organización aún no está completa."
      );
    }
    if (input.traslado.cajasTrasladadas > input.totalCajas) {
      throw new ValidacionPQRSError("Cajas trasladadas no puede superar el total de cajas.");
    }
    return this.repo.guardar(input);
  }
}
""",
    "src/domain/entities/AyudaDeMemoria.ts": """// Espejo exacto del formato institucional GD-040 "Ayuda de Memoria" de la SDIS. Los nombres de
// campo siguen la plantilla real (Lugar, Tema, Desarrollo, Asistentes, Compromisos, Proxima
// reunion, Elaboro) para que el PDF que genera la PWA se vea igual al que ya usa el equipo --
// no una reinterpretacion mia del formato.

export interface AsistenteActa {
  nombre: string;
  cargoRol: string;
  /** "No aplica" si es usuario o beneficiario (asi lo indica la plantilla original). */
  dependencia: string;
  /** Firma fisica en papel (se imprime y se firma a mano) -- por eso queda como espacio en
   *  blanco en el PDF, no como un campo de texto a llenar en la app. */
}

export interface CompromisoActa {
  actividad: string;
  responsable: string;
  fechaLimite: string; // ISO date
}

export interface AyudaDeMemoria {
  id: string;
  /** "Lugar": dependencia o entidad donde se realizo la reunion (no una direccion fisica). */
  lugar: string;
  fecha: string; // ISO date, formato de despliegue DD/MM/AAAA como pide la plantilla
  tema: string;
  /** Puntos especificos tratados u orden del dia. */
  desarrollo: string;
  asistentes: AsistenteActa[];
  compromisos: CompromisoActa[];
  /** Opcional -- la plantilla dice "si fue establecida". */
  proximaReunion?: string;
  elaboroPor: string;
  unidadOperativaId?: string; // vinculo opcional a la visita/unidad que origino la reunion
  creadoEn: string;
}

export function validarAyudaDeMemoria(a: Pick<AyudaDeMemoria, "lugar" | "fecha" | "tema" | "elaboroPor" | "asistentes">): string[] {
  const errores: string[] = [];
  if (!a.lugar?.trim()) errores.push("Lugar es obligatorio.");
  if (!a.fecha) errores.push("Fecha es obligatoria.");
  if (!a.tema?.trim()) errores.push("Tema es obligatorio.");
  if (!a.elaboroPor?.trim()) errores.push("Elaboró es obligatorio.");
  if (!a.asistentes || a.asistentes.length === 0) errores.push("Debe registrar al menos un asistente.");
  return errores;
}
""",
    "src/domain/entities/Compromiso.ts": """// Idea que ya traia el scaffold original (seguimiento de compromisos de una visita/reunion) --
// NO existe en el Excel, asi que vive aparte, sin mezclarse con RegistroPeriodo. Util para
// actas de mesas de trabajo con la Subdireccion, pero no es "avance de tareas archivisticas".

export type EstadoCompromiso = "Pendiente" | "En Proceso" | "Cumplido";

export interface Compromiso {
  id: string;
  unidadOperativaId: string;
  descripcion: string;
  responsable?: string;
  fechaLimite?: string; // ISO date
  estado: EstadoCompromiso;
  creadoEn: string;
}
""",
    "src/domain/entities/PQRS.ts": """// PQRS (Peticiones, Quejas, Reclamos y Sugerencias) vive en cada Unidad Operativa como cualquier
// otro expediente, y pasa por EL MISMO flujo de organizacion archivistico que el TRD normal
// (misma logica de tareas/porcentaje que RegistroPeriodo) -- la diferencia real esta en el
// destino final: NO es Archivo Central, es la Subsecretaria de Gestion Institucional, que es la
// responsable de su custodia. Por eso es una entidad aparte, aunque comparte estructura.
import type { TareasCantidad } from "./RegistroPeriodo";
import { calcularAvanceTotal as calcularAvanceTareas, semaforo, type Semaforo } from "./RegistroPeriodo";

export interface TrasladoPQRS {
  correoEnviado: boolean;
  fechaCorreo?: string; // ISO date -- cuando se notifico a la Subsecretaria de Gestion Institucional
  aprobado: boolean;
  fechaAprobacion?: string;
  /** El traslado en si -- distinto del traslado a Archivo Central de RegistroPeriodo. */
  trasladado: boolean;
  fechaTraslado?: string;
  cajasTrasladadas: number;
}

export interface PQRS {
  id: string;
  unidadOperativaId: string;
  /** Se cuenta en CAJAS, igual que el resto del proceso archivistico (no en carpetas). */
  totalCajas: number;
  tareas: TareasCantidad;
  traslado: TrasladoPQRS;
  encargado?: string;
  fechaVisita?: string;
  observaciones?: string;
  creadoEn: string;
  actualizadoEn: string;
}

/** Reutiliza EXACTAMENTE la misma formula de avance y el mismo semaforo de 3 colores que
 *  RegistroPeriodo -- "mismo flujo de organizacion" significa que no debe haber una regla
 *  paralela que se pueda desincronizar de la real. */
export function avanceOrganizacionPQRS(p: Pick<PQRS, "totalCajas" | "tareas">): number {
  return calcularAvanceTareas({ totalCajas: p.totalCajas, tareas: p.tareas });
}

export function semaforoPQRS(p: Pick<PQRS, "totalCajas" | "tareas">): Semaforo {
  return semaforo(avanceOrganizacionPQRS(p));
}

/** Solo se puede notificar/trasladar cuando el avance de organizacion esta completo (90%+,
 *  mismo umbral "verde" que el resto de la app) -- evita avisarle a la Subsecretaria por algo
 *  que en realidad todavia no esta listo. */
export function puedeIniciarTraslado(p: Pick<PQRS, "totalCajas" | "tareas">): boolean {
  return semaforoPQRS(p) === "verde";
}

export function cajasVigentesPQRS(p: Pick<PQRS, "totalCajas" | "traslado">): number {
  return p.totalCajas - (p.traslado?.cajasTrasladadas ?? 0);
}
""",
    "src/domain/entities/RegistroPeriodo.ts": """// Espejo de una fila de "Datos_BD" en el Excel: Unidad Operativa + Periodo TRD + visita.
// Si cambia una regla aca, cambia la MISMA regla en Calculos del Excel -- deben decir lo mismo.

export type PeriodoTRD =
  | "Fondo Acumulado (FDA)"
  | "TRD 1 (2007-2014)"
  | "TRD 2 (2014-2017)"
  | "TRD 3 (2017-2021)"
  | "TRD 4 (2021-2022)"
  | "TRD 5 (2022-2023)"
  | "TRD 6 (2023-actual)";

export const PERIODOS_TRD: PeriodoTRD[] = [
  "Fondo Acumulado (FDA)",
  "TRD 1 (2007-2014)",
  "TRD 2 (2014-2017)",
  "TRD 3 (2017-2021)",
  "TRD 4 (2021-2022)",
  "TRD 5 (2022-2023)",
  "TRD 6 (2023-actual)",
];

export interface TareasCantidad {
  fuid: number;
  /** null/undefined = "N/A" -- ese periodo no tiene nada que eliminar. Se EXCLUYE del promedio,
   *  no cuenta como 0%. Nunca fuerces un 0 aqui solo para "llenar el campo". */
  eliminacion: number | null;
  clasificacion: number;
  ordenacion: number;
  foliacion: number;
  hojaControl: number;
  rotulacion: number;
}

export type TipoAlmacenamiento =
  | "Estantería adecuada"
  | "Piso"
  | "Piso y Estantería"
  | "Lugar no apropiado";

export interface DiagnosticoRiesgo {
  tipoAlmacenamiento: TipoAlmacenamiento | null;
  riesgoHumedad: boolean | null;
  riesgoRoedores: boolean | null;
  riesgoSobreapilamiento: boolean | null;
  riesgoFiltraciones: boolean | null;
  /** Medido en sitio, NO calculado: cuantas cajas estan fuera de la estanteria. */
  cajasSobreapiladas: number;
  /** Medido en sitio, NO calculado: metros de un espacio que es de OTRA cosa (pasillo, oficina)
   *  invadidos por cajas de archivo. El mismo exceso puede apilarse en el mismo rincon (0 aqui)
   *  o regarse por una oficina entera (invade mucho) -- no hay forma de deducirlo con matematicas. */
  metrosEspacioAjenoInvadido: number;
}

export interface Transferencia {
  correoSAF: boolean;
  aprobacionSAF: boolean;
  /** Cuando esto pasa a true, ese periodo ya se trasladó al archivo central -- ver cajasTrasladadas. */
  trasladoArchivoCentral: boolean;
  /** Cuantas cajas de ESTE periodo salieron fisicamente. Total Cajas (historico) NUNCA se toca;
   *  lo que se actualiza es "Cajas Vigentes en Sitio" = totalCajas - cajasTrasladadas. */
  cajasTrasladadas: number;
}

export type EstadoVisita = "Pendiente" | "Programada" | "Realizada";

export interface RegistroPeriodo {
  id: string;
  unidadOperativaId: string;
  periodo: PeriodoTRD;
  totalCajas: number; // "Total Cajas (Meta)" -- la base de todos los porcentajes, historico, nunca se edita
  tareas: TareasCantidad;
  transferencia: Transferencia;
  diagnostico: DiagnosticoRiesgo;
  encargado?: string;
  /** undefined = Pendiente. Fecha futura = Programada. Fecha <= hoy = Realizada (ver estadoVisita()). */
  fechaVisita?: string; // ISO date (solo la fecha, sin hora)
  observaciones?: string;
  creadoEn: string; // ISO datetime
  actualizadoEn: string; // ISO datetime
}

// ---------------------------------------------------------------------------------------------
// Reglas de negocio puras -- viven en el dominio, nunca se calculan solo en la UI ni se confia
// en lo que mande el cliente. Deben coincidir exactamente con las formulas de Calculos en Excel.
// ---------------------------------------------------------------------------------------------

export function calcularAvancePorTarea(cantidad: number | null, totalCajas: number): number | null {
  if (cantidad === null || cantidad === undefined) return null; // "N/A": se excluye, no es 0%
  if (!totalCajas || totalCajas <= 0) return 0;
  return cantidad / totalCajas;
}

export function calcularAvanceTotal(r: Pick<RegistroPeriodo, "totalCajas" | "tareas">): number {
  const { tareas, totalCajas } = r;
  const valores = [
    tareas.fuid,
    tareas.eliminacion,
    tareas.clasificacion,
    tareas.ordenacion,
    tareas.foliacion,
    tareas.hojaControl,
    tareas.rotulacion,
  ];
  const porcentajes = valores
    .map((v) => calcularAvancePorTarea(v, totalCajas))
    .filter((p): p is number => p !== null); // Eliminacion en null se cae aqui, no ensucia el promedio
  if (porcentajes.length === 0) return 0;
  return porcentajes.reduce((a, b) => a + b, 0) / porcentajes.length;
}

export type Semaforo = "verde" | "ambar" | "rojo";

export function semaforo(avanceTotal: number): Semaforo {
  if (avanceTotal >= 0.9) return "verde";
  if (avanceTotal >= 0.5) return "ambar";
  return "rojo";
}

/** Nivel de riesgo de conservacion: mismo criterio de 3 colores que el semaforo de avance,
 *  para que la Directora no tenga que aprender un codigo distinto en cada parte del sistema. */
export function nivelRiesgo(d: DiagnosticoRiesgo): Semaforo | null {
  const { tipoAlmacenamiento, riesgoHumedad, riesgoRoedores, riesgoSobreapilamiento, riesgoFiltraciones } = d;
  if (
    tipoAlmacenamiento === null &&
    riesgoHumedad === null &&
    riesgoRoedores === null &&
    riesgoSobreapilamiento === null &&
    riesgoFiltraciones === null
  ) {
    return null; // aun nadie diagnostico esta unidad
  }
  let puntos = tipoAlmacenamiento === "Estantería adecuada" || tipoAlmacenamiento === null ? 0 : 2;
  if (riesgoHumedad) puntos += 1;
  if (riesgoRoedores) puntos += 1;
  if (riesgoSobreapilamiento) puntos += 1;
  if (riesgoFiltraciones) puntos += 1;
  if (puntos >= 4) return "rojo";
  if (puntos >= 2) return "ambar";
  return "verde";
}

/** Cuantas cajas quedan HOY, fisicamente, en la unidad para este periodo. El historico
 *  (totalCajas) nunca cambia; esto sí, a medida que se registran traslados. */
export function cajasVigentes(r: Pick<RegistroPeriodo, "totalCajas" | "transferencia">): number {
  return r.totalCajas - (r.transferencia?.cajasTrasladadas ?? 0);
}

/** 3 estados, no 2: una visita programada a futuro NO es lo mismo que una ya realizada. */
export function estadoVisita(fechaVisitaISO: string | undefined | null): EstadoVisita {
  if (!fechaVisitaISO) return "Pendiente";
  const fecha = new Date(fechaVisitaISO);
  if (Number.isNaN(fecha.getTime())) return "Programada"; // texto libre tipo "reprogramada"
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  return fecha.getTime() <= hoy.getTime() ? "Realizada" : "Programada";
}
""",
    "src/domain/entities/UnidadOperativa.ts": """// Entidad pura: sin dependencias de Firebase ni de React.
// Espejo del Directorio del Excel (Dependencia / Servicio / Subdireccion / Unidad + capacidad).

export type Dependencia = "SUBGIL" | "SUBICI" | "DT";

export interface CapacidadEstanteria {
  /** Medida directa con cinta metrica, si ya hay estanteria instalada. */
  metrosMedidos: number | null;
  /** Si el espacio esta vacio: largo x ancho del local, para que la calculadora estime cuanto
   *  cabria (regla AGN: ~3 metros lineales de estanteria por m2, estanteria fija de 2.20m). */
  largoEspacioM: number | null;
  anchoEspacioM: number | null;
}

export interface UnidadOperativa {
  id: string; // slug estable, ej. "subgil-cdc-kennedy-bellavista"
  dependencia: Dependencia;
  servicio: string; // "CDC" | "LAVANDERIAS COMUNITARIAS" | "EMERGENCIA SOCIAL" | "CIAM" | "SEGUIMIENTO SUBDIRECCION" | "NIVEL CENTRAL"
  subdireccionLocal: string;
  nombre: string;
  encargado?: string;
  capacidad: CapacidadEstanteria;
}

const AGN_M2_A_METROS_LINEALES = 3; // Acuerdo 049/2000 AGN: estanteria fija ~3 m lineales por m2
const CAJAS_POR_METRO_LINEAL = 4; // 4 cajas X-200 = 1 metro lineal de archivo

export function areaEspacioM2(u: Pick<UnidadOperativa, "capacidad">): number | null {
  const { largoEspacioM, anchoEspacioM } = u.capacidad;
  if (largoEspacioM == null || anchoEspacioM == null) return null;
  return largoEspacioM * anchoEspacioM;
}

export function capacidadPotencialEstimada(u: Pick<UnidadOperativa, "capacidad">): number | null {
  const area = areaEspacioM2(u);
  if (area == null) return null;
  return Math.floor(area * AGN_M2_A_METROS_LINEALES);
}

/** La medida directa manda; si no hay, cae a la calculadora (largo x ancho). */
export function capacidadEfectivaM(u: Pick<UnidadOperativa, "capacidad">): number {
  const { metrosMedidos } = u.capacidad;
  if (metrosMedidos && metrosMedidos > 0) return metrosMedidos;
  return capacidadPotencialEstimada(u) ?? 0;
}

export function metrosNecesarios(cajasVigentesTotalesUnidad: number): number {
  return Math.ceil(cajasVigentesTotalesUnidad / CAJAS_POR_METRO_LINEAL);
}

export type EstadoEspacio =
  | { tipo: "sin_dato" }
  | { tipo: "suficiente" }
  | { tipo: "insuficiente"; faltanM: number };

export function estadoEspacio(u: Pick<UnidadOperativa, "capacidad">, cajasVigentesTotalesUnidad: number): EstadoEspacio {
  const capacidad = capacidadEfectivaM(u);
  if (capacidad === 0) return { tipo: "sin_dato" };
  const necesarios = metrosNecesarios(cajasVigentesTotalesUnidad);
  if (necesarios <= capacidad) return { tipo: "suficiente" };
  return { tipo: "insuficiente", faltanM: necesarios - capacidad };
}
""",
    "src/domain/repositories/ICompromisoRepository.ts": """import type { Compromiso } from "../entities/Compromiso";

export interface ICompromisoRepository {
  listarPorUnidad(unidadOperativaId: string): Promise<Compromiso[]>;
  guardar(c: Omit<Compromiso, "id" | "creadoEn">): Promise<Compromiso>;
  actualizarEstado(id: string, estado: Compromiso["estado"]): Promise<void>;
}
""",
    "src/domain/repositories/IPQRSRepository.ts": """import type { PQRS } from "../entities/PQRS";

export interface IPQRSRepository {
  listarPorUnidad(unidadOperativaId: string): Promise<PQRS[]>;
  listarTodos(): Promise<PQRS[]>;
  guardar(p: Omit<PQRS, "id" | "creadoEn" | "actualizadoEn">): Promise<PQRS>;
  actualizar(id: string, cambios: Partial<PQRS>): Promise<void>;
}
""",
    "src/domain/repositories/IRegistroPeriodoRepository.ts": """import type { RegistroPeriodo } from "../entities/RegistroPeriodo";

// CONTRATO. El dominio y los casos de uso solo conocen esta interfaz.
// Hoy la implementa Firestore (infrastructure/repositories). Manana podria implementarla
// Azure SQL o cualquier otra cosa, sin tocar una sola linea de application/ ni presentation/.
export interface IRegistroPeriodoRepository {
  listarPorUnidad(unidadOperativaId: string): Promise<RegistroPeriodo[]>;
  /** Trae TODOS los registros -- se usa para calcular el resumen del lado del cliente (ver
   *  CalcularResumenDashboard). En el plan gratuito de Firestore no hay Cloud Functions para
   *  mantener un documento agregado, asi que el calculo se hace en el navegador, igual que
   *  hace Excel al recalcular. Para el volumen de datos de este proyecto (cientos de filas,
   *  no millones) esto es rapido y no cuesta nada extra. */
  listarTodos(): Promise<RegistroPeriodo[]>;
  listarPagina(params: {
    dependencia?: string;
    subdireccionLocal?: string;
    servicio?: string;
    periodo?: string;
    cursor?: unknown;
    tamanoPagina: number;
  }): Promise<{ items: RegistroPeriodo[]; nextCursor: unknown | null }>;
  guardar(registro: Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">): Promise<RegistroPeriodo>;
  actualizar(id: string, cambios: Partial<RegistroPeriodo>): Promise<void>;
  suscribirseAResumen(
    filtros: { dependencia?: string; subdireccionLocal?: string; servicio?: string; periodo?: string },
    onCambio: (resumen: ResumenDashboard) => void
  ): () => void; // devuelve la funcion "unsubscribe"
}

/** Documento agregado precalculado -- 1 sola lectura para pintar todo el dashboard. Espejo de
 *  las tarjetas KPI + tablas del Dashboard en Excel. */
export interface ResumenDashboard {
  cajasVigentesEnSitio: number;
  totalCajasHistorico: number;
  avancePromedioGlobal: number;
  unidadesOperativas: number;
  cajasEliminacionHistorico: number;
  cajasEliminacionEstePeriodo: number;
  unidadesEnRiesgoAlto: number;
  cajasSobreapiladas: number;
  metrosEspacioAjenoInvadido: number;
  porDependenciaServicio: Array<{
    dependencia: string;
    servicio: string;
    totalCajas: number;
    avancePromedio: number;
  }>;
  porTarea: Array<{ tarea: string; avancePromedio: number }>;
  porPeriodo: Array<{ periodo: string; totalCajas: number; avancePromedio: number }>;
  /** Nivel intermedio "por SLIS", no solo consolidado -- igual que en el Excel. */
  sobreapilamientoPorSubdireccion: Array<{
    subdireccionLocal: string;
    cajasSobreapiladas: number;
    metrosEspacioAjenoInvadido: number;
  }>;
  actualizadoEn: string;
}
""",
    "src/domain/repositories/IUnidadOperativaRepository.ts": """import type { UnidadOperativa } from "../entities/UnidadOperativa";

// El Directorio real (Dependencia -> Servicio -> Subdireccion -> Unidad), espejo exacto del
// Directorio del Excel. Vive en Firestore como un catalogo -- no cambia con cada visita, solo
// cuando se agrega/edita una unidad operativa.
export interface IUnidadOperativaRepository {
  listarTodas(): Promise<UnidadOperativa[]>;
  listarPorSubdireccion(subdireccionLocal: string): Promise<UnidadOperativa[]>;
  obtenerPorId(id: string): Promise<UnidadOperativa | null>;
  guardar(u: Omit<UnidadOperativa, "id">): Promise<UnidadOperativa>;
  actualizar(id: string, cambios: Partial<UnidadOperativa>): Promise<void>;
  /** Carga masiva -- para importar el Directorio real del Excel de una sola vez. */
  importarLote(unidades: Array<Omit<UnidadOperativa, "id">>): Promise<number>;
}
""",
    "src/domain/services/IExportadorReportes.ts": """// Mismo patron que los repositorios: el dominio solo conoce este CONTRATO. La implementacion
// real (que sabe de librerias de Excel/PDF especificas) vive en infrastructure/, para poder
// cambiar de libreria sin tocar ni un caso de uso ni una pantalla.
import type { RegistroPeriodo } from "../entities/RegistroPeriodo";
import type { PQRS } from "../entities/PQRS";
import type { AyudaDeMemoria } from "../entities/AyudaDeMemoria";

export interface IExportadorReportes {
  /** Genera un .xlsx con la misma estructura de columnas que Datos_BD en el Excel -- para que
   *  el archivo que sale de la PWA se pueda abrir y comparar directo contra el original. */
  exportarExcel(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob>;
  /** PDF de reporte para imprimir o entregar -- KPIs + tabla resumida, no la base de datos cruda. */
  exportarPDF(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob>;
  /** Ayuda de memoria: usa exactamente el formato institucional GD-040. */
  generarAyudaDeMemoria(datos: AyudaDeMemoria): Promise<Blob>;
}
""",
    "src/index.css": """@import "tailwindcss";

/* Paleta corporativa: azul (confianza, software empresarial) + teal (orden, modernidad) sobre
   grises fríos muy limpios. Escala completa alrededor de los anclajes exactos que se pidieron:
   primario #2563EB, hover #1D4ED8, secundario #0F766E. */
@theme {
  --color-primary-50: #EFF6FF;
  --color-primary-100: #DBEAFE;
  --color-primary-200: #BFDBFE;
  --color-primary-300: #93C5FD;
  --color-primary-400: #60A5FA;
  --color-primary-500: #3B82F6;
  --color-primary-600: #2563EB;
  --color-primary-700: #1D4ED8;
  --color-primary-800: #1E40AF;
  --color-primary-900: #1E3A8A;
  --color-primary-950: #172554;

  --color-accent-50: #F0FDFA;
  --color-accent-100: #CCFBF1;
  --color-accent-200: #99F6E4;
  --color-accent-300: #5EEAD4;
  --color-accent-400: #2DD4BF;
  --color-accent-500: #14B8A6;
  --color-accent-600: #0D9488;
  --color-accent-700: #0F766E;
  --color-accent-800: #115E59;
  --color-accent-900: #134E4A;

  --color-archivo-50: #F8FAFC;
  --color-archivo-100: #F1F5F9;
  --color-archivo-200: #E2E8F0;
  --color-archivo-300: #CBD5E1;
  --color-archivo-400: #94A3B8;
  --color-archivo-500: #64748B;
  --color-archivo-600: #475569;
  --color-archivo-700: #334155;
  --color-archivo-800: #1E293B;
  --color-archivo-900: #0F172A;
  --color-archivo-950: #020617;

  --color-danger: #dc2626;
}

@layer utilities {
  /* Fondo degradado suave estilo Canva: pastel, luminoso, sin la textura de cuadricula ni las
     capas de blur pesadas de antes -- mas limpio, y mas importante: SIN overflow-x:hidden (eso
     era lo que probablemente rompia el "fixed" del sidebar en algunos navegadores, al crear un
     contenedor de scroll propio que interfiere con el posicionamiento fijo). */
  .bg-documental-pattern {
    position: relative;
    background: linear-gradient(135deg, #EFF6FF 0%, #F0FDFA 45%, #F8FAFC 100%);
    background-attachment: fixed;
  }

  /* Capa lejana: manchas grandes y saturadas -- azul + teal, la paleta corporativa completa */
  .bg-documental-pattern::before {
    content: "";
    position: fixed;
    inset: -10%;
    z-index: 0;
    pointer-events: none;
    filter: blur(60px);
    background-image:
      radial-gradient(38% 32% at 8% 12%, rgba(37, 99, 235, 0.20), transparent 70%),
      radial-gradient(42% 36% at 92% 20%, rgba(15, 118, 110, 0.20), transparent 70%),
      radial-gradient(36% 34% at 20% 92%, rgba(29, 78, 216, 0.16), transparent 70%),
      radial-gradient(34% 30% at 88% 88%, rgba(13, 148, 136, 0.16), transparent 70%);
    animation: manchas-flotantes 26s ease-in-out infinite alternate;
  }

  /* Capa cercana: manchas mas chicas y nitidas, se mueven distinto -- refuerza el efecto de
     profundidad (paralaje simple con CSS, sin necesitar JS ni librerias) */
  .bg-documental-pattern::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    filter: blur(24px);
    background-image:
      radial-gradient(18% 16% at 78% 12%, rgba(59, 130, 246, 0.16), transparent 75%),
      radial-gradient(16% 14% at 15% 70%, rgba(20, 184, 166, 0.16), transparent 75%);
    animation: manchas-flotantes-cerca 18s ease-in-out infinite alternate;
  }

  /* Ilustracion de estanteria de archivo: fila completa de 4 modulos, ancla al ancho completo
     abajo (no solo una esquina) -- se nota mas, pero se mantiene a baja opacidad para que las
     tarjetas de vidrio sigan siendo lo que mas resalta. */
  .bg-documental-pattern .estanteria-ilustracion {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: min(28vw, 400px);
    z-index: 0;
    pointer-events: none;
    background-image: url("/estanteria-archivo.svg");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: bottom center;
    opacity: 0.22;
    mask-image: linear-gradient(to top, black 55%, transparent 100%);
    -webkit-mask-image: linear-gradient(to top, black 55%, transparent 100%);
  }

  .bg-documental-pattern > * {
    position: relative;
    z-index: 1;
  }
}

@keyframes manchas-flotantes {
  0%   { transform: translate(0, 0) scale(1); }
  50%  { transform: translate(-3%, 3%) scale(1.08); }
  100% { transform: translate(3%, -2%) scale(1); }
}

@keyframes manchas-flotantes-cerca {
  0%   { transform: translate(0, 0); }
  50%  { transform: translate(4%, -4%); }
  100% { transform: translate(-3%, 3%); }
}

@media (prefers-reduced-motion: reduce) {
  .bg-documental-pattern::before,
  .bg-documental-pattern::after { animation: none; }
}

/* Vidrio esmerilado real: fondo translucido (se ve el color de atras), blur fuerte, borde que
   "atrapa la luz" (linea blanca tenue arriba, como el reflejo en un vidrio real) y sombra suave
   para que flote sobre el fondo -- look premium SaaS (Stripe/Linear/Notion), no una tarjeta plana. */
.glass-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(1.4);
  -webkit-backdrop-filter: blur(20px) saturate(1.4);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow:
    0 1px 0 0 rgba(255, 255, 255, 0.8) inset,
    0 8px 30px -12px rgba(37, 99, 235, 0.16);
}

/* Tarjetas interactivas: el borde "se ilumina" (coral) y la tarjeta flota un poco mas al pasar
   el mouse -- transmite que la interfaz responde, sensacion de app sofisticada, no estatica. */
.glass-card-interactiva {
  transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
}

.glass-card-interactiva:hover {
  border-color: rgba(37, 99, 235, 0.45);
  transform: translateY(-2px);
  box-shadow:
    0 1px 0 0 rgba(255, 255, 255, 0.9) inset,
    0 0 0 1px rgba(37, 99, 235, 0.20),
    0 14px 36px -14px rgba(37, 99, 235, 0.24);
}

/* Tailwind quita el borde/apariencia nativa de los campos de formulario por diseño (Preflight) --
   sin esto, los inputs quedan funcionales pero INVISIBLES (sin borde, sin fondo distinguible).
   Esta regla les devuelve una apariencia clara y consistente en toda la app, para cualquier
   input/select/textarea, sin tener que repetir el estilo en cada pantalla. */
input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #2563EB;
}

button {
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
}""",
    "src/infrastructure/repositories/FirebasePQRSRepository.ts": """import { collection, addDoc, updateDoc, doc, query, where, getDocs, serverTimestamp, Timestamp } from "firebase/firestore";
import { db } from "../config/firebase";
import type { PQRS } from "../../domain/entities/PQRS";
import type { IPQRSRepository } from "../../domain/repositories/IPQRSRepository";

const PQRS_COLECCION = "pqrs";

function fromFirestore(id: string, data: any): PQRS {
  return {
    id,
    unidadOperativaId: data.unidadOperativaId,
    totalCajas: data.totalCajas,
    tareas: data.tareas,
    traslado: data.traslado ?? {
      correoEnviado: false, aprobado: false, trasladado: false, cajasTrasladadas: 0,
    },
    encargado: data.encargado ?? "",
    fechaVisita: data.fechaVisita ?? "",
    observaciones: data.observaciones ?? "",
    creadoEn: (data.creadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
    actualizadoEn: (data.actualizadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
  };
}

/** Misma correccion que en FirebaseRegistroPeriodoRepository: Firestore rechaza campos con
 *  valor undefined -- se limpia recursivamente antes de escribir. */
function limpiar<T extends Record<string, any>>(obj: T): T {
  const limpio: Record<string, any> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined) continue;
    limpio[k] = v && typeof v === "object" && !Array.isArray(v) ? limpiar(v) : v;
  }
  return limpio as T;
}

export class FirebasePQRSRepository implements IPQRSRepository {
  async listarPorUnidad(unidadOperativaId: string): Promise<PQRS[]> {
    const q = query(collection(db, PQRS_COLECCION), where("unidadOperativaId", "==", unidadOperativaId));
    const snap = await getDocs(q);
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async listarTodos(): Promise<PQRS[]> {
    const snap = await getDocs(collection(db, PQRS_COLECCION));
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async guardar(p: Omit<PQRS, "id" | "creadoEn" | "actualizadoEn">): Promise<PQRS> {
    const ref = await addDoc(collection(db, PQRS_COLECCION), {
      ...limpiar(p),
      creadoEn: serverTimestamp(),
      actualizadoEn: serverTimestamp(),
    });
    return { ...p, id: ref.id, creadoEn: new Date().toISOString(), actualizadoEn: new Date().toISOString() };
  }

  async actualizar(id: string, cambios: Partial<PQRS>): Promise<void> {
    await updateDoc(doc(db, PQRS_COLECCION, id), { ...limpiar(cambios), actualizadoEn: serverTimestamp() });
  }
}
""",
    "src/infrastructure/repositories/FirebaseRegistroPeriodoRepository.ts": """import {
  collection,
  doc,
  addDoc,
  updateDoc,
  query,
  where,
  limit,
  startAfter,
  getDocs,
  onSnapshot,
  serverTimestamp,
  Timestamp,
} from "firebase/firestore";
import { db } from "../config/firebase";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import type {
  IRegistroPeriodoRepository,
  ResumenDashboard,
} from "../../domain/repositories/IRegistroPeriodoRepository";

const REGISTROS = "registrosPeriodo";
const RESUMENES = "resumenes"; // 1 documento por Dependencia (o "GLOBAL"), recalculado al guardar

function fromFirestore(id: string, data: any): RegistroPeriodo {
  return {
    id,
    unidadOperativaId: data.unidadOperativaId,
    periodo: data.periodo,
    totalCajas: data.totalCajas,
    tareas: data.tareas,
    transferencia: data.transferencia ?? {
      correoSAF: false,
      aprobacionSAF: false,
      trasladoArchivoCentral: false,
      cajasTrasladadas: 0,
    },
    diagnostico: data.diagnostico ?? {
      tipoAlmacenamiento: null,
      riesgoHumedad: null,
      riesgoRoedores: null,
      riesgoSobreapilamiento: null,
      riesgoFiltraciones: null,
      cajasSobreapiladas: 0,
      metrosEspacioAjenoInvadido: 0,
    },
    encargado: data.encargado ?? "",
    fechaVisita: data.fechaVisita ?? "",
    observaciones: data.observaciones ?? "",
    creadoEn: (data.creadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
    actualizadoEn: (data.actualizadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
  };
}

// Implementa el CONTRATO del dominio. Esta es la UNICA clase del proyecto que sabe
// que "por debajo" hay Firestore. Si manana migras a otra base, solo se reemplaza este archivo.
export class FirebaseRegistroPeriodoRepository implements IRegistroPeriodoRepository {
  async listarPorUnidad(unidadOperativaId: string): Promise<RegistroPeriodo[]> {
    const q = query(collection(db, REGISTROS), where("unidadOperativaId", "==", unidadOperativaId));
    const snap = await getDocs(q);
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async listarTodos(): Promise<RegistroPeriodo[]> {
    const snap = await getDocs(collection(db, REGISTROS));
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async listarPagina({
    dependencia,
    subdireccionLocal,
    servicio,
    periodo,
    cursor,
    tamanoPagina,
  }: Parameters<IRegistroPeriodoRepository["listarPagina"]>[0]) {
    const clauses: any[] = [];
    if (dependencia) clauses.push(where("dependencia", "==", dependencia));
    if (subdireccionLocal) clauses.push(where("subdireccionLocal", "==", subdireccionLocal));
    if (servicio) clauses.push(where("servicio", "==", servicio));
    if (periodo) clauses.push(where("periodo", "==", periodo));

    let q = query(collection(db, REGISTROS), ...clauses, limit(tamanoPagina));
    if (cursor) q = query(q, startAfter(cursor));

    const snap = await getDocs(q);
    const items = snap.docs.map((d) => fromFirestore(d.id, d.data()));
    const nextCursor = snap.docs.length === tamanoPagina ? snap.docs[snap.docs.length - 1] : null;
    return { items, nextCursor };
  }

  /** Firestore RECHAZA cualquier campo con valor `undefined` (el error que viste: "Unsupported
   *  field value: undefined"). En JS/TS es comun terminar con undefined en campos opcionales que
   *  el usuario no lleno (encargado, fechaVisita, observaciones) -- esta funcion los quita antes
   *  de escribir, recursivamente, para que nunca vuelva a pasar sin importar que campo se agregue
   *  despues. */
  private limpiar<T extends Record<string, any>>(obj: T): T {
    const limpio: Record<string, any> = {};
    for (const [k, v] of Object.entries(obj)) {
      if (v === undefined) continue;
      limpio[k] = v && typeof v === "object" && !Array.isArray(v) && !(v instanceof Date)
        ? this.limpiar(v)
        : v;
    }
    return limpio as T;
  }

  async guardar(registro: Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">): Promise<RegistroPeriodo> {
    const ref = await addDoc(collection(db, REGISTROS), {
      ...this.limpiar(registro),
      creadoEn: serverTimestamp(),
      actualizadoEn: serverTimestamp(),
    });
    // El recalculo del "resumen" agregado se dispara aqui mismo (barato) o via Cloud Function
    // (mas robusto si varias personas guardan al mismo tiempo). Empieza simple, migra si hace falta.
    return { ...registro, id: ref.id, creadoEn: new Date().toISOString(), actualizadoEn: new Date().toISOString() };
  }

  async actualizar(id: string, cambios: Partial<RegistroPeriodo>): Promise<void> {
    await updateDoc(doc(db, REGISTROS, id), { ...this.limpiar(cambios), actualizadoEn: serverTimestamp() });
  }

  suscribirseAResumen(
    filtros: { dependencia?: string; subdireccionLocal?: string },
    onCambio: (resumen: ResumenDashboard) => void
  ): () => void {
    // UNA sola lectura en tiempo real sobre UN documento agregado -- nunca sobre la coleccion cruda.
    const docId = filtros.dependencia ?? "GLOBAL";
    const unsub = onSnapshot(doc(db, RESUMENES, docId), (snap) => {
      if (snap.exists()) onCambio(snap.data() as ResumenDashboard);
    });
    return unsub;
  }
}
""",
    "src/infrastructure/repositories/FirebaseUnidadOperativaRepository.ts": """import { collection, doc, addDoc, updateDoc, getDoc, getDocs, query, where, writeBatch } from "firebase/firestore";
import { db } from "../config/firebase";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";
import type { IUnidadOperativaRepository } from "../../domain/repositories/IUnidadOperativaRepository";

const COLECCION = "unidadesOperativas";

function fromFirestore(id: string, data: any): UnidadOperativa {
  return {
    id,
    dependencia: data.dependencia,
    servicio: data.servicio,
    subdireccionLocal: data.subdireccionLocal,
    nombre: data.nombre,
    encargado: data.encargado ?? "",
    capacidad: data.capacidad ?? { metrosMedidos: null, largoEspacioM: null, anchoEspacioM: null },
  };
}

export class FirebaseUnidadOperativaRepository implements IUnidadOperativaRepository {
  async listarTodas(): Promise<UnidadOperativa[]> {
    const snap = await getDocs(collection(db, COLECCION));
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async listarPorSubdireccion(subdireccionLocal: string): Promise<UnidadOperativa[]> {
    const q = query(collection(db, COLECCION), where("subdireccionLocal", "==", subdireccionLocal));
    const snap = await getDocs(q);
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async obtenerPorId(id: string): Promise<UnidadOperativa | null> {
    const snap = await getDoc(doc(db, COLECCION, id));
    return snap.exists() ? fromFirestore(snap.id, snap.data()) : null;
  }

  async guardar(u: Omit<UnidadOperativa, "id">): Promise<UnidadOperativa> {
    const ref = await addDoc(collection(db, COLECCION), u);
    return { ...u, id: ref.id };
  }

  async actualizar(id: string, cambios: Partial<UnidadOperativa>): Promise<void> {
    await updateDoc(doc(db, COLECCION, id), cambios);
  }

  /** Escribe en lotes de 500 (limite de Firestore por batch) -- para importar el Directorio
   *  completo del Excel de una sola vez sin agotar la cuota con cientos de escrituras sueltas. */
  async importarLote(unidades: Array<Omit<UnidadOperativa, "id">>): Promise<number> {
    let escritas = 0;
    for (let i = 0; i < unidades.length; i += 500) {
      const lote = unidades.slice(i, i + 500);
      const batch = writeBatch(db);
      for (const u of lote) {
        const ref = doc(collection(db, COLECCION));
        batch.set(ref, u);
      }
      await batch.commit();
      escritas += lote.length;
    }
    return escritas;
  }
}
""",
    "src/infrastructure/repositories/MockRegistroPeriodoRepository.ts": """// Implementacion en memoria -- util para desarrollar la UI sin gastar cuota de Firestore,
// y para pruebas. Implementa el MISMO contrato que la version real.
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import type {
  IRegistroPeriodoRepository,
  ResumenDashboard,
} from "../../domain/repositories/IRegistroPeriodoRepository";

export class MockRegistroPeriodoRepository implements IRegistroPeriodoRepository {
  private registros: RegistroPeriodo[] = [];
  private idSeq = 1;

  async listarPorUnidad(unidadOperativaId: string): Promise<RegistroPeriodo[]> {
    return this.registros.filter((r) => r.unidadOperativaId === unidadOperativaId);
  }

  async listarTodos(): Promise<RegistroPeriodo[]> {
    return [...this.registros];
  }

  async listarPagina(params: Parameters<IRegistroPeriodoRepository["listarPagina"]>[0]) {
    let items = [...this.registros];
    if (params.periodo) items = items.filter((r) => r.periodo === params.periodo);
    const pagina = items.slice(0, params.tamanoPagina);
    return { items: pagina, nextCursor: null };
  }

  async guardar(registro: Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">): Promise<RegistroPeriodo> {
    const ahora = new Date().toISOString();
    const nuevo: RegistroPeriodo = { ...registro, id: String(this.idSeq++), creadoEn: ahora, actualizadoEn: ahora };
    this.registros.push(nuevo);
    return nuevo;
  }

  async actualizar(id: string, cambios: Partial<RegistroPeriodo>): Promise<void> {
    const idx = this.registros.findIndex((r) => r.id === id);
    if (idx >= 0) this.registros[idx] = { ...this.registros[idx], ...cambios, actualizadoEn: new Date().toISOString() };
  }

  suscribirseAResumen(_filtros: unknown, onCambio: (resumen: ResumenDashboard) => void): () => void {
    onCambio({
      cajasVigentesEnSitio: 0, totalCajasHistorico: 0, avancePromedioGlobal: 0, unidadesOperativas: 0,
      cajasEliminacionHistorico: 0, cajasEliminacionEstePeriodo: 0, unidadesEnRiesgoAlto: 0,
      cajasSobreapiladas: 0, metrosEspacioAjenoInvadido: 0,
      porDependenciaServicio: [], porTarea: [], porPeriodo: [], sobreapilamientoPorSubdireccion: [],
      actualizadoEn: new Date().toISOString(),
    });
    return () => {};
  }
}
""",
    "src/infrastructure/services/JsPDFExportadorReportes.ts": """// Implementacion CONCRETA del contrato IExportadorReportes usando jsPDF + jspdf-autotable +
// xlsx. Esta es la UNICA clase del proyecto que sabe que existen esas librerias especificas --
// si mañana se cambia de libreria, solo se toca este archivo.
//
// Requiere instalar las dependencias primero:
//   npm install xlsx jspdf jspdf-autotable
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { calcularAvanceTotal, cajasVigentes } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import { avanceOrganizacionPQRS, cajasVigentesPQRS } from "../../domain/entities/PQRS";
import type { AyudaDeMemoria } from "../../domain/entities/AyudaDeMemoria";
import type { IExportadorReportes } from "../../domain/services/IExportadorReportes";

function formatearFecha(iso?: string): string {
  if (!iso) return "";
  const [a, m, d] = iso.split("-");
  return d && m && a ? `${d}/${m}/${a}` : iso;
}

export class JsPDFExportadorReportes implements IExportadorReportes {
  async exportarExcel(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob> {
    // Mismas columnas conceptuales que Datos_BD en el Excel original, para poder comparar
    // directo el archivo que sale de la PWA contra el que ya conoce el equipo.
    const filas = registros.map((r) => ({
      "Unidad Operativa": r.unidadOperativaId,
      "Periodo / Fase": r.periodo,
      "Total Cajas (Meta)": r.totalCajas,
      "FUID (Cant)": r.tareas.fuid,
      "Eliminación (Cant)": r.tareas.eliminacion ?? "N/A",
      "Clasificación (Cant)": r.tareas.clasificacion,
      "Ordenación (Cant)": r.tareas.ordenacion,
      "Foliación (Cant)": r.tareas.foliacion,
      "Hoja de Control (Cant)": r.tareas.hojaControl,
      "Rotulación (Cant)": r.tareas.rotulacion,
      "% Avance Total": calcularAvanceTotal(r),
      "Cajas Vigentes en Sitio": cajasVigentes(r),
      "Encargado": r.encargado ?? "",
      "Fecha Visita": formatearFecha(r.fechaVisita),
      "Observaciones": r.observaciones ?? "",
    }));
    const filasPQRS = pqrs.map((p) => ({
      "Unidad Operativa": p.unidadOperativaId,
      "Total Cajas PQRS": p.totalCajas,
      "% Avance Organización": avanceOrganizacionPQRS(p),
      "Cajas Vigentes PQRS": cajasVigentesPQRS(p),
      "Notificado Subsecretaría": p.traslado.correoEnviado ? "SI" : "NO",
      "Trasladado": p.traslado.trasladado ? "SI" : "NO",
    }));

    const libro = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(libro, XLSX.utils.json_to_sheet(filas), "Datos_BD");
    XLSX.utils.book_append_sheet(libro, XLSX.utils.json_to_sheet(filasPQRS), "PQRS");
    const buffer = XLSX.write(libro, { bookType: "xlsx", type: "array" });
    return new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
  }

  async exportarPDF(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob> {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Reporte de Gestión Documental — Pérgamo", 14, 18);
    doc.setFontSize(10);
    doc.text(`Generado: ${new Date().toLocaleDateString("es-CO")}`, 14, 25);

    autoTable(doc, {
      startY: 32,
      head: [["Unidad Operativa", "Periodo", "Total Cajas", "% Avance", "Cajas Vigentes"]],
      body: registros.map((r) => [
        r.unidadOperativaId, r.periodo, r.totalCajas,
        `${Math.round(calcularAvanceTotal(r) * 100)}%`, cajasVigentes(r),
      ]),
      headStyles: { fillColor: [37, 99, 235] },
    });

    if (pqrs.length > 0) {
      const finalY = (doc as any).lastAutoTable.finalY + 10;
      doc.setFontSize(12);
      doc.text("PQRS", 14, finalY);
      autoTable(doc, {
        startY: finalY + 4,
        head: [["Unidad Operativa", "Total Cajas", "% Avance", "Notificado", "Trasladado"]],
        body: pqrs.map((p) => [
          p.unidadOperativaId, p.totalCajas,
          `${Math.round(avanceOrganizacionPQRS(p) * 100)}%`,
          p.traslado.correoEnviado ? "Sí" : "No",
          p.traslado.trasladado ? "Sí" : "No",
        ]),
        headStyles: { fillColor: [15, 118, 110] },
      });
    }
    return doc.output("blob");
  }

  /** Formato institucional GD-040 exacto: Lugar / Fecha / Tema / Desarrollo / tabla de
   *  Asistentes (con espacio en blanco para firma física) / tabla de Compromisos / Próxima
   *  reunión / Elaboró. */
  async generarAyudaDeMemoria(datos: AyudaDeMemoria): Promise<Blob> {
    const doc = new jsPDF();
    let y = 18;

    doc.setFontSize(15);
    doc.text("Ayuda de Memoria", 14, y);
    y += 10;

    doc.setFontSize(10);
    const campo = (etiqueta: string, valor: string) => {
      doc.setFont("helvetica", "bold");
      doc.text(`${etiqueta}:`, 14, y);
      doc.setFont("helvetica", "normal");
      const lineas = doc.splitTextToSize(valor || "", 150);
      doc.text(lineas, 45, y);
      y += Math.max(6, lineas.length * 5);
    };
    campo("Lugar", datos.lugar);
    campo("Fecha", formatearFecha(datos.fecha));
    campo("Tema", datos.tema);
    campo("Desarrollo", datos.desarrollo);
    y += 4;

    doc.setFont("helvetica", "bold");
    doc.text("Asistentes", 14, y);
    y += 2;
    autoTable(doc, {
      startY: y,
      head: [["Nombre", "Cargo/Rol", "Dependencia", "Firma"]],
      body: datos.asistentes.map((a) => [a.nombre, a.cargoRol, a.dependencia, ""]), // firma en blanco -- se firma a mano
      headStyles: { fillColor: [37, 99, 235] },
      columnStyles: { 3: { minCellHeight: 14 } }, // deja espacio real para firmar a mano
    });
    y = (doc as any).lastAutoTable.finalY + 8;

    doc.setFont("helvetica", "bold");
    doc.text("Compromisos", 14, y);
    y += 2;
    autoTable(doc, {
      startY: y,
      head: [["Actividad", "Responsable", "Fecha límite"]],
      body: datos.compromisos.map((c) => [c.actividad, c.responsable, formatearFecha(c.fechaLimite)]),
      headStyles: { fillColor: [37, 99, 235] },
    });
    y = (doc as any).lastAutoTable.finalY + 10;

    doc.setFont("helvetica", "normal");
    campo("Próxima reunión", datos.proximaReunion ? formatearFecha(datos.proximaReunion) : "No establecida");
    campo("Elaboró", datos.elaboroPor);

    return doc.output("blob");
  }
}
""",
    "src/main.tsx": """import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { FormularioVisita } from '@presentation/screens/FormularioVisita';
import { PQRSPage } from '@presentation/screens/PQRSPage';
import { AyudaDeMemoriaPage } from '@presentation/screens/AyudaDeMemoriaPage';
import { DirectorioPage } from '@presentation/screens/DirectorioPage';
import { TableroPage } from '@presentation/screens/TableroPage';
import { Navbar } from '@presentation/components/Navbar';
import type { Vista } from '@presentation/components/Navbar';
// @ts-ignore
import './index.css';

function App() {
  const [vista, setVista] = useState<Vista>("captura");

  return (
    <div className="min-h-screen bg-documental-pattern text-slate-900 pb-16">
      <div className="estanteria-ilustracion" aria-hidden="true" />
      <Navbar vista={vista} onCambiarVista={setVista} />

      <main className="mx-auto max-w-3xl px-4 pt-32 sm:pt-24">
        {vista === "captura" && <FormularioVisita />}
        {vista === "pqrs" && <PQRSPage />}
        {vista === "ayuda-memoria" && <AyudaDeMemoriaPage />}
        {vista === "directorio" && <DirectorioPage />}
        {vista === "tablero" && <TableroPage />}
      </main>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",
    "src/presentation/components/Navbar.tsx": """import { useState } from "react";

export type Vista = "captura" | "pqrs" | "ayuda-memoria" | "directorio" | "tablero";

interface SubItem {
  vista: Vista;
  label: string;
  descripcion: string;
  disponible: boolean;
}

interface ItemMenu {
  id: string;
  label: string;
  submenus: SubItem[];
}

const MENU: ItemMenu[] = [
  {
    id: "captura",
    label: "Captura",
    submenus: [
      { vista: "captura", label: "Nueva visita", descripcion: "Registrar avance de una unidad operativa", disponible: true },
      { vista: "pqrs", label: "PQRS", descripcion: "Organización y traslado a Gestión Institucional", disponible: true },
      { vista: "ayuda-memoria", label: "Ayuda de memoria", descripcion: "Generar PDF con el formato GD-040", disponible: true },
    ],
  },
  {
    id: "directorio",
    label: "Directorio",
    submenus: [
      { vista: "directorio", label: "Catálogo de unidades", descripcion: "SLIS, CDC, Lavanderías, CIAM — importar y consultar", disponible: true },
    ],
  },
  {
    id: "tablero",
    label: "Tablero",
    submenus: [
      { vista: "tablero", label: "Resumen general", descripcion: "KPIs consolidados, igual que el Excel", disponible: false },
    ],
  },
];

/** A que grupo del menu pertenece la vista activa -- para resaltar el boton padre correcto. */
function grupoDe(vista: Vista): string {
  return MENU.find((m) => m.submenus.some((s) => s.vista === vista))?.id ?? "captura";
}

export function Navbar({ vista, onCambiarVista }: { vista: Vista; onCambiarVista: (v: Vista) => void }) {
  const [abierto, setAbierto] = useState<string | null>(null);
  const grupoActivo = grupoDe(vista);

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      {/* Banner superior: franja institucional alusiva a gestion documental. Texto mas corto
          en movil -- el completo no cabe en una linea y se veia cortado feo. */}
      <div className="bg-gradient-to-r from-primary-900 via-primary-800 to-primary-700 text-primary-50">
        <div className="mx-auto flex max-w-5xl items-center justify-center gap-2 px-4 py-1.5 text-xs font-medium tracking-wide">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="shrink-0 opacity-80">
            <path d="M4 4h16v16H4z" strokeLinejoin="round" />
            <path d="M4 9h16M9 4v16" />
          </svg>
          <span className="hidden sm:inline">Trazabilidad TRD de principio a fin — de la visita en sitio al tablero de la Dirección</span>
          <span className="sm:hidden">Trazabilidad TRD, de la visita al tablero</span>
        </div>
      </div>

      {/* Barra principal */}
      <div className="glass-card border-b border-white/40 shadow-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-primary-700 to-primary-500 text-xl font-black text-white shadow-md">
              P
            </div>
            <div>
              <h1 className="text-lg font-bold leading-none text-primary-950 sm:text-xl">Pérgamo</h1>
              <p className="mt-0.5 text-[11px] font-medium text-slate-500 sm:text-xs">Sistema de Auditoría &amp; Gestión Documental</p>
            </div>
          </div>

          {/* Menu con submenus (desktop) -- cada submenu navega a su propia vista */}
          <nav className="hidden items-center gap-1 sm:flex">
            {MENU.map((item) => (
              <div
                key={item.id}
                className="relative"
                onMouseEnter={() => setAbierto(item.id)}
                onMouseLeave={() => setAbierto(null)}
              >
                <button
                  onClick={() => onCambiarVista(item.submenus[0].vista)}
                  className={`rounded-lg px-3 py-2 text-sm font-semibold transition ${
                    grupoActivo === item.id ? "bg-primary-700 text-white" : "text-slate-700 hover:bg-primary-50"
                  }`}
                >
                  {item.label}
                </button>
                {abierto === item.id && (
                  <div className="absolute left-0 top-full w-72 pt-2">
                    <div className="glass-card overflow-hidden rounded-xl p-1.5 shadow-lg">
                      {item.submenus.map((sub) => (
                        <div
                          key={sub.vista}
                          className={`rounded-lg px-3 py-2 text-sm ${
                            sub.disponible ? "cursor-pointer hover:bg-primary-50" : "cursor-default opacity-50"
                          } ${vista === sub.vista ? "bg-primary-50" : ""}`}
                          onClick={() => sub.disponible && onCambiarVista(sub.vista)}
                        >
                          <div className="flex items-center justify-between font-semibold text-slate-800">
                            {sub.label}
                            {!sub.disponible && (
                              <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-500">
                                Próximamente
                              </span>
                            )}
                          </div>
                          <p className="mt-0.5 text-xs text-slate-500">{sub.descripcion}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </nav>

          <span className="hidden items-center gap-1.5 rounded-full border border-primary-200 bg-primary-100 px-3 py-1 text-xs font-semibold text-primary-800 sm:inline-flex">
            <span className="h-2 w-2 animate-pulse rounded-full bg-primary-500" />
            PWA Activa
          </span>
        </div>

        {/* Menu movil: acordeon simple, ya que ahora hay submenus reales de verdad */}
        <div className="flex flex-wrap gap-1 border-t border-white/40 px-4 py-2 sm:hidden">
          {MENU.flatMap((item) => item.submenus.filter((s) => s.disponible)).map((sub) => (
            <button
              key={sub.vista}
              onClick={() => onCambiarVista(sub.vista)}
              className={`rounded-lg px-2.5 py-1.5 text-xs font-semibold transition ${
                vista === sub.vista ? "bg-primary-700 text-white" : "bg-white/60 text-slate-700"
              }`}
            >
              {sub.label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
""",
    "src/presentation/components/Sidebar.tsx": """import { useState, type ReactNode } from "react";
import type { Vista } from "./Navbar";

interface ItemNav {
  id: Vista;
  label: string;
  icono: ReactNode;
  submenus: Array<{ label: string; descripcion: string; disponible: boolean }>;
}

const iconoCaptura = (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 20h9" /><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z" />
  </svg>
);
const iconoTablero = (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" /><path d="M9 3v18M3 9h6" />
  </svg>
);

const NAV: ItemNav[] = [
  {
    id: "captura", label: "Captura", icono: iconoCaptura,
    submenus: [
      { label: "Nueva visita", descripcion: "Registrar avance de una unidad operativa", disponible: true },
      { label: "Historial de visitas", descripcion: "Ver capturas anteriores por unidad", disponible: false },
    ],
  },
  {
    id: "tablero", label: "Tablero", icono: iconoTablero,
    submenus: [
      { label: "Resumen general", descripcion: "KPIs consolidados, igual que el Excel", disponible: false },
      { label: "Por Subdirección", descripcion: "Desglose SLIS, sobreapilamiento, avance", disponible: false },
      { label: "Por Unidad Operativa", descripcion: "Detalle unidad por unidad", disponible: false },
    ],
  },
];

/** Sidebar fijo estilo Canva: barra vertical de iconos a la izquierda, siempre en su sitio
 *  (position: fixed, left:0, alto completo). Estructuralmente mucho mas simple que un header de
 *  2 pisos -- un solo elemento fijo, sin banners apilados -- por eso es mas dificil que un bug
 *  de CSS lo desalinee. En movil se colapsa a una barra inferior (mismo patron que apps como
 *  Instagram/Notion en celular). */
export function Sidebar({ vista, onCambiarVista }: { vista: Vista; onCambiarVista: (v: Vista) => void }) {
  const [abierto, setAbierto] = useState<Vista | null>(null);

  return (
    <>
      {/* Desktop: columna fija a la izquierda -- mas compacta: los botones son cuadrados
          ajustados al icono (no bloques que estiran todo el ancho), con un divisor bajo el
          logo y un icono de ayuda anclado abajo para que el sidebar no se sienta vacio. */}
      <aside className="fixed inset-y-0 left-0 z-50 hidden w-[72px] flex-col items-center bg-archivo-900 sm:flex">
        <div className="flex h-16 w-full items-center justify-center">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary-600 text-sm font-black text-white">
            P
          </div>
        </div>
        <div className="mx-3 h-px w-8 bg-white/10" />

        <nav className="flex flex-1 flex-col items-center gap-2 pt-4">
          {NAV.map((item) => (
            <div
              key={item.id}
              className="group relative"
              onMouseEnter={() => setAbierto(item.id)}
              onMouseLeave={() => setAbierto(null)}
            >
              <button
                onClick={() => onCambiarVista(item.id)}
                className={`flex h-11 w-11 items-center justify-center rounded-xl transition ${
                  vista === item.id
                    ? "bg-primary-600 text-white shadow-md shadow-primary-900/40"
                    : "text-slate-400 hover:bg-white/[0.06] hover:text-white"
                }`}
                title={item.label}
              >
                {item.icono}
              </button>
              <p className={`mt-1 text-center text-[10px] font-semibold ${vista === item.id ? "text-white" : "text-slate-500"}`}>
                {item.label}
              </p>

              {abierto === item.id && (
                <div className="absolute left-full top-0 z-10 pl-2">
                  <div className="glass-card w-64 overflow-hidden rounded-xl p-1.5 shadow-lg">
                    {item.submenus.map((sub) => (
                      <div
                        key={sub.label}
                        className={`rounded-lg px-3 py-2 text-sm ${
                          sub.disponible ? "cursor-pointer hover:bg-primary-50" : "cursor-default opacity-50"
                        }`}
                        onClick={() => sub.disponible && onCambiarVista(item.id)}
                      >
                        <div className="flex items-center justify-between font-semibold text-slate-800">
                          {sub.label}
                          {!sub.disponible && (
                            <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-500">
                              Próximamente
                            </span>
                          )}
                        </div>
                        <p className="mt-0.5 text-xs text-slate-500">{sub.descripcion}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </nav>

        {/* Ancla la parte inferior -- evita el vacio que se veia antes bajo el menu */}
        <div className="flex flex-col items-center gap-3 pb-4">
          <button className="flex h-9 w-9 items-center justify-center rounded-full text-slate-500 transition hover:bg-white/[0.06] hover:text-white" title="Ayuda">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" /><path d="M9.5 9a2.5 2.5 0 0 1 4.9.8c0 1.7-2.4 1.9-2.4 3.4" /><path d="M12 17.5v.01" />
            </svg>
          </button>
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-accent-600 text-xs font-bold text-white" title="Elmer Cabrera">
            EC
          </div>
        </div>
      </aside>

      {/* Movil: barra fija abajo */}
      <nav className="fixed inset-x-0 bottom-0 z-50 flex border-t border-white/50 bg-white/85 backdrop-blur-xl sm:hidden">
        {NAV.map((item) => (
          <button
            key={item.id}
            onClick={() => onCambiarVista(item.id)}
            className={`flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[11px] font-semibold transition ${
              vista === item.id ? "text-primary-700" : "text-slate-500"
            }`}
          >
            {item.icono}
            {item.label}
          </button>
        ))}
      </nav>
    </>
  );
}
""",
    "src/presentation/hooks/useAyudaDeMemoria.ts": """import { useMemo, useState } from "react";
import type { AyudaDeMemoria } from "../../domain/entities/AyudaDeMemoria";
import { validarAyudaDeMemoria } from "../../domain/entities/AyudaDeMemoria";
import { JsPDFExportadorReportes } from "../../infrastructure/services/JsPDFExportadorReportes";

export const useAyudaDeMemoria = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const exportador = useMemo(() => new JsPDFExportadorReportes(), []);

  const generarPDF = async (datos: Omit<AyudaDeMemoria, "id" | "creadoEn">) => {
    setError(null);
    const errores = validarAyudaDeMemoria(datos);
    if (errores.length > 0) {
      setError(errores.join(" "));
      throw new Error(errores.join(" "));
    }
    setLoading(true);
    try {
      const completa: AyudaDeMemoria = { ...datos, id: "", creadoEn: new Date().toISOString() };
      const blob = await exportador.generarAyudaDeMemoria(completa);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `ayuda-de-memoria-${datos.fecha || "sin-fecha"}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } finally {
      setLoading(false);
    }
  };

  return { generarPDF, loading, error };
};
""",
    "src/presentation/hooks/useDirectorio.ts": """import { useEffect, useMemo, useState } from "react";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";
import { FirebaseUnidadOperativaRepository } from "../../infrastructure/repositories/FirebaseUnidadOperativaRepository";

/** Trae el catalogo completo de unidades operativas (el "Directorio") una sola vez y lo deja en
 *  memoria -- se usa para armar los selectores en cascada Subdireccion -> Servicio -> Unidad en
 *  toda la app, sin repetir la consulta a Firestore en cada pantalla. */
export function useDirectorio() {
  const [unidades, setUnidades] = useState<UnidadOperativa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const repo = useMemo(() => new FirebaseUnidadOperativaRepository(), []);

  async function recargar() {
    setLoading(true);
    setError(null);
    try {
      setUnidades(await repo.listarTodas());
    } catch (err: any) {
      setError(err.message || "No se pudo cargar el Directorio.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { recargar(); }, []);

  const subdirecciones = useMemo(
    () => Array.from(new Set(unidades.map((u) => u.subdireccionLocal))).sort(),
    [unidades]
  );

  function serviciosDe(subdireccionLocal: string) {
    return Array.from(new Set(unidades.filter((u) => u.subdireccionLocal === subdireccionLocal).map((u) => u.servicio))).sort();
  }

  function unidadesDe(subdireccionLocal: string, servicio: string) {
    return unidades.filter((u) => u.subdireccionLocal === subdireccionLocal && u.servicio === servicio);
  }

  return { unidades, subdirecciones, serviciosDe, unidadesDe, loading, error, recargar, repo };
}
""",
    "src/presentation/hooks/usePQRS.ts": """import { useState, useMemo } from "react";
import type { PQRS } from "../../domain/entities/PQRS";
import { RegistrarPQRS, type RegistrarPQRSInput } from "../../application/useCases/RegistrarPQRS";
import { FirebasePQRSRepository } from "../../infrastructure/repositories/FirebasePQRSRepository";

export const usePQRS = () => {
  const [items, setItems] = useState<PQRS[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registrarPQRS = useMemo(() => {
    const repository = new FirebasePQRSRepository();
    return new RegistrarPQRS(repository);
  }, []);

  const registrar = async (input: RegistrarPQRSInput) => {
    setLoading(true);
    setError(null);
    try {
      const nuevo = await registrarPQRS.ejecutar(input);
      setItems((prev) => [nuevo, ...prev]);
      return nuevo;
    } catch (err: any) {
      setError(err.message || "Error al conectar con la base de datos");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { items, loading, error, registrar };
};
""",
    "src/presentation/hooks/useRegistroPeriodo.ts": """import { useState, useMemo } from "react";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { RegistrarAvancePeriodo, type RegistrarAvanceInput } from "../../application/useCases/RegistrarAvancePeriodo";
import { FirebaseRegistroPeriodoRepository } from "../../infrastructure/repositories/FirebaseRegistroPeriodoRepository";

export const useRegistroPeriodo = () => {
  const [registros, setRegistros] = useState<RegistroPeriodo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registrarAvancePeriodo = useMemo(() => {
    const repository = new FirebaseRegistroPeriodoRepository();
    return new RegistrarAvancePeriodo(repository);
  }, []);

  const registrar = async (input: RegistrarAvanceInput) => {
    setLoading(true);
    setError(null);
    try {
      const nuevo = await registrarAvancePeriodo.ejecutar(input);
      setRegistros((prev) => [nuevo, ...prev]);
      return nuevo;
    } catch (err: any) {
      setError(err.message || "Error al conectar con la base de datos");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { registros, loading, error, registrar };
};
""",
    "src/presentation/hooks/useTablero.ts": """import { useEffect, useMemo, useState } from "react";
import { FirebaseRegistroPeriodoRepository } from "../../infrastructure/repositories/FirebaseRegistroPeriodoRepository";
import { FirebasePQRSRepository } from "../../infrastructure/repositories/FirebasePQRSRepository";
import { calcularResumenDashboard } from "../../application/services/CalcularResumenDashboard";
import type { ResumenDashboard } from "../../domain/repositories/IRegistroPeriodoRepository";

/** Trae TODOS los registros y PQRS, y calcula el resumen en el navegador -- ver la nota en
 *  CalcularResumenDashboard sobre por que no hay un documento pre-agregado (Firestore free
 *  tier no tiene Cloud Functions). Se puede llamar "refrescar" despues de cada captura nueva
 *  para que el Tablero se vea actualizado sin recargar la pagina entera. */
export function useTablero() {
  const [resumen, setResumen] = useState<ResumenDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const repos = useMemo(() => ({
    registros: new FirebaseRegistroPeriodoRepository(),
    pqrs: new FirebasePQRSRepository(),
  }), []);

  async function refrescar() {
    setLoading(true);
    setError(null);
    try {
      const [registros, pqrs] = await Promise.all([
        repos.registros.listarTodos(),
        repos.pqrs.listarTodos(),
      ]);
      setResumen(calcularResumenDashboard(registros, pqrs));
    } catch (err: any) {
      setError(err.message || "No se pudo cargar el tablero.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refrescar();
  }, []);

  return { resumen, loading, error, refrescar };
}
""",
    "src/presentation/screens/AyudaDeMemoriaPage.tsx": """import { useState } from "react";
import { useAyudaDeMemoria } from "../hooks/useAyudaDeMemoria";
import type { AsistenteActa, CompromisoActa } from "../../domain/entities/AyudaDeMemoria";

const campoBase =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 " +
  "shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";
const etiqueta = "block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1.5";

function Tarjeta({ children }: { children: React.ReactNode }) {
  return <section className="glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6">{children}</section>;
}

const ASISTENTE_VACIO: AsistenteActa = { nombre: "", cargoRol: "", dependencia: "" };
const COMPROMISO_VACIO: CompromisoActa = { actividad: "", responsable: "", fechaLimite: "" };

/** Formato institucional GD-040: Lugar / Fecha / Tema / Desarrollo / Asistentes (filas
 *  dinamicas, "Inserte tantas filas como requiera" dice la plantilla) / Compromisos (mismo
 *  patron) / Proxima reunion / Elaboro. */
export function AyudaDeMemoriaPage() {
  const { generarPDF, loading, error } = useAyudaDeMemoria();
  const [lugar, setLugar] = useState("");
  const [fecha, setFecha] = useState("");
  const [tema, setTema] = useState("");
  const [desarrollo, setDesarrollo] = useState("");
  const [asistentes, setAsistentes] = useState<AsistenteActa[]>([{ ...ASISTENTE_VACIO }]);
  const [compromisos, setCompromisos] = useState<CompromisoActa[]>([{ ...COMPROMISO_VACIO }]);
  const [proximaReunion, setProximaReunion] = useState("");
  const [elaboroPor, setElaboroPor] = useState("");
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);

  function actualizarAsistente(i: number, campo: keyof AsistenteActa, valor: string) {
    setAsistentes(asistentes.map((a, idx) => (idx === i ? { ...a, [campo]: valor } : a)));
  }
  function actualizarCompromiso(i: number, campo: keyof CompromisoActa, valor: string) {
    setCompromisos(compromisos.map((c, idx) => (idx === i ? { ...c, [campo]: valor } : c)));
  }

  async function generar() {
    setMensaje(null);
    try {
      await generarPDF({
        lugar, fecha, tema, desarrollo,
        asistentes: asistentes.filter((a) => a.nombre.trim() !== ""),
        compromisos: compromisos.filter((c) => c.actividad.trim() !== ""),
        proximaReunion: proximaReunion || undefined,
        elaboroPor,
      });
      setMensaje({ tipo: "ok", texto: "PDF generado y descargado con el formato institucional GD-040." });
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo generar el PDF." });
    }
  }

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Ayuda de memoria</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Formato GD-040</h1>
        <p className="mt-1 text-sm text-slate-500">Genera el PDF con el mismo formato institucional que ya usa el equipo.</p>
      </div>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Lugar</span>
            <input className={campoBase} value={lugar} onChange={(e) => setLugar(e.target.value)}
                   placeholder="Dependencia o entidad donde se realizó la reunión" />
          </label>
          <label className="block">
            <span className={etiqueta}>Fecha</span>
            <input type="date" className={campoBase} value={fecha} onChange={(e) => setFecha(e.target.value)} />
          </label>
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Tema</span>
            <input className={campoBase} value={tema} onChange={(e) => setTema(e.target.value)}
                   placeholder="Objetivo de la reunión" />
          </label>
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Desarrollo</span>
            <textarea className={campoBase} rows={4} value={desarrollo} onChange={(e) => setDesarrollo(e.target.value)}
                       placeholder="Puntos específicos tratados u orden del día" />
          </label>
        </div>
      </Tarjeta>

      <Tarjeta>
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-700">Asistentes</p>
          <button onClick={() => setAsistentes([...asistentes, { ...ASISTENTE_VACIO }])}
                  className="text-xs font-semibold text-primary-600 hover:text-primary-700">
            + Agregar asistente
          </button>
        </div>
        <div className="space-y-3">
          {asistentes.map((a, i) => (
            <div key={i} className="grid grid-cols-[1fr_1fr_1fr_auto] items-end gap-2 border-b border-slate-100 pb-3">
              <label className="block">
                <span className="text-[10px] text-slate-400">Nombre</span>
                <input className={campoBase} value={a.nombre} onChange={(e) => actualizarAsistente(i, "nombre", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Cargo/Rol</span>
                <input className={campoBase} value={a.cargoRol} onChange={(e) => actualizarAsistente(i, "cargoRol", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Dependencia</span>
                <input className={campoBase} value={a.dependencia} onChange={(e) => actualizarAsistente(i, "dependencia", e.target.value)}
                       placeholder="No aplica si es usuario/beneficiario" />
              </label>
              <button onClick={() => setAsistentes(asistentes.filter((_, idx) => idx !== i))}
                      disabled={asistentes.length === 1}
                      className="h-9 rounded-lg px-2 text-xs text-red-500 hover:bg-red-50 disabled:opacity-30">
                Quitar
              </button>
            </div>
          ))}
        </div>
        <p className="mt-2 text-xs text-slate-400">La firma queda en blanco en el PDF — se firma físicamente en papel.</p>
      </Tarjeta>

      <Tarjeta>
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-700">Compromisos</p>
          <button onClick={() => setCompromisos([...compromisos, { ...COMPROMISO_VACIO }])}
                  className="text-xs font-semibold text-primary-600 hover:text-primary-700">
            + Agregar compromiso
          </button>
        </div>
        <div className="space-y-3">
          {compromisos.map((c, i) => (
            <div key={i} className="grid grid-cols-[1.5fr_1fr_1fr_auto] items-end gap-2 border-b border-slate-100 pb-3">
              <label className="block">
                <span className="text-[10px] text-slate-400">Actividad</span>
                <input className={campoBase} value={c.actividad} onChange={(e) => actualizarCompromiso(i, "actividad", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Responsable</span>
                <input className={campoBase} value={c.responsable} onChange={(e) => actualizarCompromiso(i, "responsable", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Fecha límite</span>
                <input type="date" className={campoBase} value={c.fechaLimite} onChange={(e) => actualizarCompromiso(i, "fechaLimite", e.target.value)} />
              </label>
              <button onClick={() => setCompromisos(compromisos.filter((_, idx) => idx !== i))}
                      disabled={compromisos.length === 1}
                      className="h-9 rounded-lg px-2 text-xs text-red-500 hover:bg-red-50 disabled:opacity-30">
                Quitar
              </button>
            </div>
          ))}
        </div>
      </Tarjeta>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Próxima reunión</span>
            <input type="date" className={campoBase} value={proximaReunion} onChange={(e) => setProximaReunion(e.target.value)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Elaboró</span>
            <input className={campoBase} value={elaboroPor} onChange={(e) => setElaboroPor(e.target.value)} />
          </label>
        </div>
      </Tarjeta>

      {(mensaje || error) && (
        <div className={`rounded-lg border px-4 py-3 text-sm ${
          mensaje?.tipo === "ok" ? "border-green-200 bg-green-50 text-green-700" : "border-red-200 bg-red-50 text-red-700"
        }`}>
          {mensaje?.texto ?? error}
        </div>
      )}

      <button onClick={generar} disabled={loading}
        className="w-full sm:w-auto rounded-xl bg-primary-700 px-6 py-3 text-sm font-semibold text-white shadow-md
                   transition hover:bg-primary-800 disabled:cursor-not-allowed disabled:bg-slate-300">
        {loading ? "Generando…" : "Generar PDF"}
      </button>
    </div>
  );
}
""",
    "src/presentation/screens/DirectorioPage.tsx": """import { useRef, useState } from "react";
import { useDirectorio } from "../hooks/useDirectorio";
import type { UnidadOperativa, Dependencia } from "../../domain/entities/UnidadOperativa";

function Tarjeta({ children }: { children: React.ReactNode }) {
  return <section className="glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6">{children}</section>;
}

/** Parsea un CSV con columnas: Dependencia,Servicio,Subdireccion,Nombre,Encargado
 *  (encabezado obligatorio, en ese orden -- exportable directo desde la hoja "Directorio" del
 *  Excel: Dependencia | Servicio | Subdirección Local | Unidad Operativa | Encargado). */
function parsearCSV(texto: string): Array<Omit<UnidadOperativa, "id">> {
  const lineas = texto.split(/\\r?\\n/).filter((l) => l.trim() !== "");
  const filas = lineas.slice(1); // salta encabezado
  return filas.map((linea) => {
    const [dependencia, servicio, subdireccionLocal, nombre, encargado] = linea.split(",").map((c) => c.trim());
    return {
      dependencia: dependencia as Dependencia,
      servicio, subdireccionLocal, nombre,
      encargado: encargado || undefined,
      capacidad: { metrosMedidos: null, largoEspacioM: null, anchoEspacioM: null },
    };
  }).filter((u) => u.nombre);
}

/** Pantalla para importar el Directorio REAL (Dependencia/Servicio/Subdirección/Unidad) desde
 *  un CSV exportado del Excel -- para no inventar nombres de unidades institucionales, cada
 *  SLIS/CDC/Lavandería/CIAM que la app conoce viene directo de tus datos reales. */
export function DirectorioPage() {
  const { unidades, subdirecciones, loading, recargar, repo } = useDirectorio();
  const [importando, setImportando] = useState(false);
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function manejarArchivo(e: React.ChangeEvent<HTMLInputElement>) {
    const archivo = e.target.files?.[0];
    if (!archivo) return;
    setImportando(true);
    setMensaje(null);
    try {
      const texto = await archivo.text();
      const filas = parsearCSV(texto);
      if (filas.length === 0) throw new Error("El archivo no tiene filas válidas. Revisa el formato de columnas.");
      const escritas = await repo.importarLote(filas);
      setMensaje({ tipo: "ok", texto: `${escritas} unidades importadas correctamente.` });
      await recargar();
    } catch (err) {
      setMensaje({ tipo: "error", texto: err instanceof Error ? err.message : "No se pudo importar el archivo." });
    } finally {
      setImportando(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Directorio</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Catálogo de unidades operativas</h1>
        <p className="mt-1 text-sm text-slate-500">
          SLIS, CDC, Lavanderías, CIAM y demás — el mismo Directorio del Excel, importado una sola vez.
        </p>
      </div>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Importar desde CSV</p>
        <p className="mt-1 text-xs text-slate-500">
          Exporta la hoja "Directorio" del Excel a CSV con las columnas, en este orden:{" "}
          <code className="rounded bg-slate-100 px-1 py-0.5 text-[11px]">Dependencia,Servicio,Subdireccion,Nombre,Encargado</code>
        </p>
        <input
          ref={inputRef} type="file" accept=".csv" onChange={manejarArchivo} disabled={importando}
          className="mt-3 block w-full text-sm text-slate-600 file:mr-3 file:rounded-lg file:border-0 file:bg-primary-600 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-primary-700"
        />
        {importando && <p className="mt-2 text-xs text-slate-400">Importando…</p>}
        {mensaje && (
          <p className={`mt-2 text-sm ${mensaje.tipo === "ok" ? "text-green-600" : "text-red-600"}`}>{mensaje.texto}</p>
        )}
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">
          {loading ? "Cargando…" : `${unidades.length} unidades en ${subdirecciones.length} subdirecciones`}
        </p>
        {!loading && unidades.length === 0 && (
          <p className="text-sm text-slate-400">
            Todavía no hay unidades importadas. Sube el CSV de arriba para empezar.
          </p>
        )}
        {subdirecciones.map((sub) => (
          <div key={sub} className="mb-3 border-b border-slate-100 pb-3 last:border-0">
            <p className="text-sm font-semibold text-slate-700">{sub}</p>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {unidades.filter((u) => u.subdireccionLocal === sub).map((u) => (
                <span key={u.id} className="rounded-full bg-primary-50 px-2.5 py-1 text-xs text-primary-700">
                  {u.servicio} · {u.nombre}
                </span>
              ))}
            </div>
          </div>
        ))}
      </Tarjeta>
    </div>
  );
}
""",
    "src/presentation/screens/FormularioVisita.tsx": """import { useMemo, useState } from "react";
import { useRegistroPeriodo } from "../hooks/useRegistroPeriodo";
import { useDirectorio } from "../hooks/useDirectorio";
import {
  calcularAvancePorTarea,
  calcularAvanceTotal,
  semaforo,
  PERIODOS_TRD,
} from "../../domain/entities/RegistroPeriodo";
import type {
  PeriodoTRD,
  TareasCantidad,
  Transferencia,
  DiagnosticoRiesgo,
  TipoAlmacenamiento,
} from "../../domain/entities/RegistroPeriodo";

const PERIODOS = PERIODOS_TRD;

const TAREAS: Array<{ key: keyof TareasCantidad; label: string; opcional?: boolean }> = [
  { key: "fuid", label: "FUID" },
  { key: "eliminacion", label: "Eliminación", opcional: true },
  { key: "clasificacion", label: "Clasificación" },
  { key: "ordenacion", label: "Ordenación" },
  { key: "foliacion", label: "Foliación" },
  { key: "hojaControl", label: "Hoja de Control" },
  { key: "rotulacion", label: "Rotulación" },
];

const VACIAS: TareasCantidad = {
  fuid: 0, eliminacion: null, clasificacion: 0, ordenacion: 0,
  foliacion: 0, hojaControl: 0, rotulacion: 0,
};
const TRANSFERENCIA_VACIA: Transferencia = {
  correoSAF: false, aprobacionSAF: false, trasladoArchivoCentral: false, cajasTrasladadas: 0,
};
const DIAGNOSTICO_VACIO: DiagnosticoRiesgo = {
  tipoAlmacenamiento: null,
  riesgoHumedad: null, riesgoRoedores: null, riesgoSobreapilamiento: null, riesgoFiltraciones: null,
  cajasSobreapiladas: 0, metrosEspacioAjenoInvadido: 0,
};
const TIPOS_ALMACENAMIENTO: TipoAlmacenamiento[] = [
  "Estantería adecuada", "Piso", "Piso y Estantería", "Lugar no apropiado",
];

const SEMAFORO_ESTILO = {
  verde: { punto: "bg-emerald-500", texto: "text-emerald-700", fondo: "bg-emerald-50", borde: "border-emerald-200" },
  ambar: { punto: "bg-amber-500", texto: "text-amber-700", fondo: "bg-amber-50", borde: "border-amber-200" },
  rojo: { punto: "bg-red-500", texto: "text-red-700", fondo: "bg-red-50", borde: "border-red-200" },
} as const;

const campoBase =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 " +
  "shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";
const etiqueta = "block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1.5";

function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <section className={`glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6 ${className}`}>
      {children}
    </section>
  );
}

export function FormularioVisita() {
  const { registrar, loading } = useRegistroPeriodo();
  const { subdirecciones, serviciosDe, unidadesDe, loading: cargandoDirectorio } = useDirectorio();
  const [subdireccionSel, setSubdireccionSel] = useState("");
  const [servicioSel, setServicioSel] = useState("");
  const [unidadOperativaId, setUnidad] = useState("");
  const [periodo, setPeriodo] = useState<PeriodoTRD>(PERIODOS[0]);
  const [totalCajas, setTotalCajas] = useState<number>(0);
  const [tareas, setTareas] = useState<TareasCantidad>(VACIAS);
  const [transferencia, setTransferencia] = useState<Transferencia>(TRANSFERENCIA_VACIA);
  const [diagnostico, setDiagnostico] = useState<DiagnosticoRiesgo>(DIAGNOSTICO_VACIO);
  const [encargado, setEncargado] = useState("");
  const [fechaVisita, setFechaVisita] = useState("");
  const [observaciones, setObservaciones] = useState("");
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);

  const serviciosDisponibles = subdireccionSel ? serviciosDe(subdireccionSel) : [];
  const unidadesDisponibles = subdireccionSel && servicioSel ? unidadesDe(subdireccionSel, servicioSel) : [];

  const avanceTotal = useMemo(() => calcularAvanceTotal({ totalCajas, tareas }), [totalCajas, tareas]);
  const estado = semaforo(avanceTotal);
  const estiloEstado = SEMAFORO_ESTILO[estado];

  const excedidas = TAREAS.filter(
    ({ key }) => totalCajas > 0 && typeof tareas[key] === "number" && (tareas[key] as number) > totalCajas
  );

  async function guardar() {
    setMensaje(null);
    try {
      await registrar({
        unidadOperativaId, periodo, totalCajas, tareas, transferencia, diagnostico,
        encargado: encargado || undefined,
        fechaVisita: fechaVisita || undefined,
        observaciones: observaciones || undefined,
      });
      setMensaje({ tipo: "ok", texto: "Visita registrada. El tablero ya refleja el cambio." });
      setTareas(VACIAS); setTotalCajas(0);
      setTransferencia(TRANSFERENCIA_VACIA); setDiagnostico(DIAGNOSTICO_VACIO);
      setObservaciones(""); setFechaVisita("");
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo guardar." });
    }
  }

  const puedeGuardar = unidadOperativaId.trim() !== "" && totalCajas > 0 && excedidas.length === 0 && !loading;

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Registro de visita</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Capturar avance por periodo</h1>
        <p className="mt-1 text-sm text-slate-500">Digita solo cantidades de cajas. Los porcentajes se calculan solos.</p>
      </div>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-3">
          <label className="block">
            <span className={etiqueta}>Subdirección Local</span>
            <select className={campoBase} value={subdireccionSel}
                    onChange={(e) => { setSubdireccionSel(e.target.value); setServicioSel(""); setUnidad(""); }}
                    disabled={cargandoDirectorio}>
              <option value="">{cargandoDirectorio ? "Cargando…" : "Selecciona…"}</option>
              {subdirecciones.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Servicio</span>
            <select className={campoBase} value={servicioSel} disabled={!subdireccionSel}
                    onChange={(e) => { setServicioSel(e.target.value); setUnidad(""); }}>
              <option value="">{subdireccionSel ? "Selecciona…" : "Elige subdirección primero"}</option>
              {serviciosDisponibles.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Unidad operativa</span>
            <select className={campoBase} value={unidadOperativaId} disabled={!servicioSel}
                    onChange={(e) => setUnidad(e.target.value)}>
              <option value="">{servicioSel ? "Selecciona…" : "Elige servicio primero"}</option>
              {unidadesDisponibles.map((u) => <option key={u.id} value={u.id}>{u.nombre}</option>)}
            </select>
            {servicioSel && unidadesDisponibles.length === 0 && (
              <p className="mt-1 text-xs text-amber-600">No hay unidades registradas aquí — impórtalas en "Directorio".</p>
            )}
          </label>
          <label className="block">
            <span className={etiqueta}>Periodo / fase TRD</span>
            <select className={campoBase} value={periodo} onChange={(e) => setPeriodo(e.target.value as PeriodoTRD)}>
              {PERIODOS.map((p) => <option key={p} value={p}>{p}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Total cajas (meta)</span>
            <input type="number" min={0} className={`${campoBase} font-mono text-base`}
                   value={totalCajas || ""} onChange={(e) => setTotalCajas(Number(e.target.value) || 0)} />
          </label>
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Fecha de la visita</span>
            <input type="date" className={`${campoBase} max-w-xs`} value={fechaVisita}
                   onChange={(e) => setFechaVisita(e.target.value)} />
            <span className="mt-1 block text-xs text-slate-400">
              En blanco = Pendiente. Futura = Programada. Hoy o antes = Realizada.
            </span>
          </label>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Cajas completadas por tarea</p>
        <div className="space-y-3">
          {TAREAS.map(({ key, label, opcional }) => {
            const valor = tareas[key];
            const esNA = opcional && (valor === null || valor === undefined);
            const pct = calcularAvancePorTarea(valor, totalCajas);
            const excede = totalCajas > 0 && typeof valor === "number" && valor > totalCajas;
            return (
              <div key={key} className="flex items-center gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-700">{label}</span>
                    {opcional && (
                      <label className="flex items-center gap-1.5 text-xs text-slate-400">
                        <input type="checkbox" checked={!!esNA}
                               onChange={(e) => setTareas({ ...tareas, [key]: e.target.checked ? null : 0 })} />
                        N/A
                      </label>
                    )}
                  </div>
                  <div className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
                    <div
                      className={`h-full rounded-full transition-all ${excede ? "bg-red-500" : "bg-primary-500"}`}
                      style={{ width: `${Math.min(pct ?? 0, 1) * 100}%` }}
                    />
                  </div>
                </div>
                <input
                  type="number" min={0} disabled={!!esNA} aria-label={`Cajas de ${label}`}
                  className={`w-20 rounded-lg border px-2 py-1.5 text-right text-sm font-mono shadow-sm
                    focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:bg-slate-50 disabled:text-slate-300
                    ${excede ? "border-red-400 ring-1 ring-red-400" : "border-slate-300 focus:border-primary-500"}`}
                  value={esNA ? "" : (valor ?? 0) || ""}
                  onChange={(e) => setTareas({ ...tareas, [key]: Number(e.target.value) || 0 })}
                />
                <span className="w-11 shrink-0 text-right text-sm font-mono text-slate-500">
                  {pct === null ? "N/A" : `${Math.round(pct * 100)}%`}
                </span>
              </div>
            );
          })}
        </div>
        {excedidas.length > 0 && (
          <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
            <p className="text-xs font-bold uppercase tracking-wide text-red-700">Revisa estas cantidades</p>
            <p className="mt-1 text-sm text-red-700">
              {excedidas.map((t) => t.label).join(", ")} supera{excedidas.length > 1 ? "n" : ""} las{" "}
              <span className="font-mono">{totalCajas}</span> cajas del periodo.
            </p>
          </div>
        )}
      </Tarjeta>

      <Tarjeta className={`flex items-center gap-4 ${estiloEstado.fondo} ${estiloEstado.borde}`}>
        <div className={`h-3 w-3 shrink-0 rounded-full ${estiloEstado.punto}`} />
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Avance total del periodo</p>
          <p className={`font-mono text-3xl font-bold ${estiloEstado.texto}`}>{Math.round(avanceTotal * 100)}%</p>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Transferencia al archivo central</p>
        <p className="mt-1 text-xs text-slate-400">
          Se activa solo cuando el periodo llegó al 100% y ya se trasladó. El histórico nunca cambia.
        </p>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
          {([
            ["correoSAF", "Correo SAF"],
            ["aprobacionSAF", "Aprobación SAF"],
            ["trasladoArchivoCentral", "Traslado Archivo Central"],
          ] as const).map(([key, label]) => (
            <label key={key} className="flex items-center gap-2 text-sm text-slate-700">
              <input type="checkbox" checked={transferencia[key]}
                     onChange={(e) => setTransferencia({ ...transferencia, [key]: e.target.checked })} />
              {label}
            </label>
          ))}
        </div>
        {transferencia.trasladoArchivoCentral && (
          <label className="mt-3 block max-w-[220px]">
            <span className={etiqueta}>Cajas trasladadas</span>
            <input type="number" min={0} max={totalCajas} className={campoBase}
                   value={transferencia.cajasTrasladadas || ""}
                   onChange={(e) => setTransferencia({ ...transferencia, cajasTrasladadas: Number(e.target.value) || 0 })} />
          </label>
        )}
      </Tarjeta>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Diagnóstico de conservación (esta visita)</p>
        <label className="mt-3 block max-w-xs">
          <span className={etiqueta}>Tipo de almacenamiento</span>
          <select className={campoBase} value={diagnostico.tipoAlmacenamiento ?? ""}
                  onChange={(e) => setDiagnostico({ ...diagnostico, tipoAlmacenamiento: (e.target.value || null) as TipoAlmacenamiento | null })}>
            <option value="">Sin diagnosticar</option>
            {TIPOS_ALMACENAMIENTO.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
          {([
            ["riesgoHumedad", "Humedad"],
            ["riesgoRoedores", "Roedores"],
            ["riesgoSobreapilamiento", "Sobreapilamiento"],
            ["riesgoFiltraciones", "Filtraciones / lluvias"],
          ] as const).map(([key, label]) => (
            <label key={key} className="flex items-center gap-2 text-sm text-slate-700">
              <input type="checkbox" checked={diagnostico[key] === true}
                     onChange={(e) => setDiagnostico({ ...diagnostico, [key]: e.target.checked })} />
              {label}
            </label>
          ))}
        </div>
        {diagnostico.riesgoSobreapilamiento && (
          <div className="mt-4 grid gap-4 border-t border-slate-100 pt-4 sm:grid-cols-2">
            <label className="block">
              <span className={etiqueta}>Cajas sobreapiladas (fuera de estantería)</span>
              <input type="number" min={0} className={campoBase}
                     value={diagnostico.cajasSobreapiladas || ""}
                     onChange={(e) => setDiagnostico({ ...diagnostico, cajasSobreapiladas: Number(e.target.value) || 0 })} />
            </label>
            <label className="block">
              <span className={etiqueta}>Metros de espacio ajeno invadido</span>
              <input type="number" min={0} step={0.1} className={campoBase}
                     value={diagnostico.metrosEspacioAjenoInvadido || ""}
                     onChange={(e) => setDiagnostico({ ...diagnostico, metrosEspacioAjenoInvadido: Number(e.target.value) || 0 })} />
              <span className="mt-1 block text-xs text-slate-400">
                Pasillo, oficina u otro espacio que no es de archivo. 0 si el exceso está en el mismo rincón.
              </span>
            </label>
          </div>
        )}
      </Tarjeta>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Encargado</span>
            <input className={campoBase} value={encargado} onChange={(e) => setEncargado(e.target.value)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Observaciones</span>
            <textarea className={campoBase} rows={2} value={observaciones}
                      onChange={(e) => setObservaciones(e.target.value)}
                      placeholder="Novedades de la visita (opcional)" />
          </label>
        </div>
      </Tarjeta>

      {mensaje && (
        <div className={`rounded-lg border px-4 py-3 text-sm ${
          mensaje.tipo === "ok" ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-red-200 bg-red-50 text-red-700"
        }`}>
          {mensaje.texto}
        </div>
      )}

      <button
        onClick={guardar}
        disabled={!puedeGuardar}
        className="w-full sm:w-auto rounded-xl bg-primary-700 px-6 py-3 text-sm font-semibold text-white shadow-md
                   transition hover:bg-primary-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
      >
        {loading ? "Guardando…" : "Registrar visita"}
      </button>
    </div>
  );
}
""",
    "src/presentation/screens/PQRSPage.tsx": """import { useMemo, useState } from "react";
import { usePQRS } from "../hooks/usePQRS";
import { useDirectorio } from "../hooks/useDirectorio";
import {
  calcularAvancePorTarea,
  calcularAvanceTotal,
  semaforo,
} from "../../domain/entities/RegistroPeriodo";
import type { TareasCantidad, Semaforo } from "../../domain/entities/RegistroPeriodo";
import type { TrasladoPQRS } from "../../domain/entities/PQRS";
import { puedeIniciarTraslado } from "../../domain/entities/PQRS";

const TAREAS: Array<{ key: keyof TareasCantidad; label: string; opcional?: boolean }> = [
  { key: "fuid", label: "FUID" },
  { key: "eliminacion", label: "Eliminación", opcional: true },
  { key: "clasificacion", label: "Clasificación" },
  { key: "ordenacion", label: "Ordenación" },
  { key: "foliacion", label: "Foliación" },
  { key: "hojaControl", label: "Hoja de Control" },
  { key: "rotulacion", label: "Rotulación" },
];

const VACIAS: TareasCantidad = {
  fuid: 0, eliminacion: null, clasificacion: 0, ordenacion: 0,
  foliacion: 0, hojaControl: 0, rotulacion: 0,
};
const TRASLADO_VACIO: TrasladoPQRS = {
  correoEnviado: false, aprobado: false, trasladado: false, cajasTrasladadas: 0,
};

const COLOR_SEMAFORO: Record<Semaforo, string> = {
  verde: "#16A34A", ambar: "#F59E0B", rojo: "#DC2626",
};

const campoBase =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 " +
  "shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";
const etiqueta = "block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1.5";

function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6 ${className}`}>{children}</section>;
}

export function PQRSPage() {
  const { registrar, loading } = usePQRS();
  const { subdirecciones, serviciosDe, unidadesDe, loading: cargandoDirectorio } = useDirectorio();
  const [subdireccionSel, setSubdireccionSel] = useState("");
  const [servicioSel, setServicioSel] = useState("");
  const [unidadOperativaId, setUnidad] = useState("");
  const [totalCajas, setTotalCajas] = useState<number>(0);
  const [tareas, setTareas] = useState<TareasCantidad>(VACIAS);
  const [traslado, setTraslado] = useState<TrasladoPQRS>(TRASLADO_VACIO);
  const [encargado, setEncargado] = useState("");
  const [fechaVisita, setFechaVisita] = useState("");
  const [observaciones, setObservaciones] = useState("");
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);

  const serviciosDisponibles = subdireccionSel ? serviciosDe(subdireccionSel) : [];
  const unidadesDisponibles = subdireccionSel && servicioSel ? unidadesDe(subdireccionSel, servicioSel) : [];

  const avanceTotal = useMemo(() => calcularAvanceTotal({ totalCajas, tareas }), [totalCajas, tareas]);
  const estado = semaforo(avanceTotal);
  const listoParaTraslado = puedeIniciarTraslado({ totalCajas, tareas });

  const excedidas = TAREAS.filter(
    ({ key }) => totalCajas > 0 && typeof tareas[key] === "number" && (tareas[key] as number) > totalCajas
  );

  async function guardar() {
    setMensaje(null);
    try {
      await registrar({
        unidadOperativaId, totalCajas, tareas, traslado,
        encargado: encargado || undefined,
        fechaVisita: fechaVisita || undefined,
        observaciones: observaciones || undefined,
      });
      setMensaje({ tipo: "ok", texto: "PQRS registrado. El tablero ya refleja el cambio." });
      setTareas(VACIAS); setTotalCajas(0); setTraslado(TRASLADO_VACIO);
      setObservaciones(""); setFechaVisita("");
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo guardar." });
    }
  }

  const puedeGuardar = unidadOperativaId.trim() !== "" && totalCajas > 0 && excedidas.length === 0 && !loading;

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Registro de PQRS</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Organización y traslado de PQRS</h1>
        <p className="mt-1 text-sm text-slate-500">
          Mismo flujo de organización que el TRD normal — se cuenta en cajas. El destino final es
          la Subsecretaría de Gestión Institucional, no el Archivo Central.
        </p>
      </div>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-3">
          <label className="block">
            <span className={etiqueta}>Subdirección Local</span>
            <select className={campoBase} value={subdireccionSel}
                    onChange={(e) => { setSubdireccionSel(e.target.value); setServicioSel(""); setUnidad(""); }}
                    disabled={cargandoDirectorio}>
              <option value="">{cargandoDirectorio ? "Cargando…" : "Selecciona…"}</option>
              {subdirecciones.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Servicio</span>
            <select className={campoBase} value={servicioSel} disabled={!subdireccionSel}
                    onChange={(e) => { setServicioSel(e.target.value); setUnidad(""); }}>
              <option value="">{subdireccionSel ? "Selecciona…" : "Elige subdirección primero"}</option>
              {serviciosDisponibles.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Unidad operativa</span>
            <select className={campoBase} value={unidadOperativaId} disabled={!servicioSel}
                    onChange={(e) => setUnidad(e.target.value)}>
              <option value="">{servicioSel ? "Selecciona…" : "Elige servicio primero"}</option>
              {unidadesDisponibles.map((u) => <option key={u.id} value={u.id}>{u.nombre}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Total cajas PQRS</span>
            <input type="number" min={0} className={`${campoBase} font-mono text-base`}
                   value={totalCajas || ""} onChange={(e) => setTotalCajas(Number(e.target.value) || 0)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Fecha de la visita</span>
            <input type="date" className={campoBase} value={fechaVisita} onChange={(e) => setFechaVisita(e.target.value)} />
          </label>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Cajas organizadas por tarea</p>
        <div className="space-y-3">
          {TAREAS.map(({ key, label, opcional }) => {
            const valor = tareas[key];
            const esNA = opcional && (valor === null || valor === undefined);
            const pct = calcularAvancePorTarea(valor, totalCajas);
            const excede = totalCajas > 0 && typeof valor === "number" && valor > totalCajas;
            return (
              <div key={key} className="flex items-center gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-700">{label}</span>
                    {opcional && (
                      <label className="flex items-center gap-1.5 text-xs text-slate-400">
                        <input type="checkbox" checked={!!esNA}
                               onChange={(e) => setTareas({ ...tareas, [key]: e.target.checked ? null : 0 })} />
                        N/A
                      </label>
                    )}
                  </div>
                  <div className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
                    <div className={`h-full rounded-full transition-all ${excede ? "bg-red-500" : "bg-primary-500"}`}
                         style={{ width: `${Math.min(pct ?? 0, 1) * 100}%` }} />
                  </div>
                </div>
                <input type="number" min={0} disabled={!!esNA} aria-label={`Cajas de ${label}`}
                  className={`w-20 rounded-lg border px-2 py-1.5 text-right text-sm font-mono shadow-sm
                    focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:bg-slate-50 disabled:text-slate-300
                    ${excede ? "border-red-400 ring-1 ring-red-400" : "border-slate-300 focus:border-primary-500"}`}
                  value={esNA ? "" : (valor ?? 0) || ""}
                  onChange={(e) => setTareas({ ...tareas, [key]: Number(e.target.value) || 0 })} />
                <span className="w-11 shrink-0 text-right text-sm font-mono text-slate-500">
                  {pct === null ? "N/A" : `${Math.round(pct * 100)}%`}
                </span>
              </div>
            );
          })}
        </div>
        {excedidas.length > 0 && (
          <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
            <p className="text-sm text-red-700">
              {excedidas.map((t) => t.label).join(", ")} supera{excedidas.length > 1 ? "n" : ""} el total de cajas.
            </p>
          </div>
        )}
      </Tarjeta>

      <Tarjeta className="flex items-center gap-4">
        <div className="h-3 w-3 shrink-0 rounded-full" style={{ background: COLOR_SEMAFORO[estado] }} />
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Avance de organización</p>
          <p className="font-mono text-3xl font-bold" style={{ color: COLOR_SEMAFORO[estado] }}>
            {Math.round(avanceTotal * 100)}%
          </p>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Traslado a Subsecretaría de Gestión Institucional</p>
        <p className="mt-1 text-xs text-slate-400">
          {listoParaTraslado
            ? "La organización está completa — ya se puede notificar y trasladar."
            : "Solo se habilita cuando el avance de organización llega al 90% o más."}
        </p>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
          {([
            ["correoEnviado", "Correo enviado"],
            ["aprobado", "Aprobado"],
            ["trasladado", "Trasladado"],
          ] as const).map(([key, label]) => (
            <label key={key} className={`flex items-center gap-2 text-sm ${listoParaTraslado ? "text-slate-700" : "text-slate-300"}`}>
              <input type="checkbox" checked={traslado[key]} disabled={!listoParaTraslado}
                     onChange={(e) => setTraslado({ ...traslado, [key]: e.target.checked })} />
              {label}
            </label>
          ))}
        </div>
        {traslado.trasladado && (
          <label className="mt-3 block max-w-[220px]">
            <span className={etiqueta}>Cajas trasladadas</span>
            <input type="number" min={0} max={totalCajas} className={campoBase}
                   value={traslado.cajasTrasladadas || ""}
                   onChange={(e) => setTraslado({ ...traslado, cajasTrasladadas: Number(e.target.value) || 0 })} />
          </label>
        )}
      </Tarjeta>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Encargado</span>
            <input className={campoBase} value={encargado} onChange={(e) => setEncargado(e.target.value)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Observaciones</span>
            <textarea className={campoBase} rows={2} value={observaciones} onChange={(e) => setObservaciones(e.target.value)} />
          </label>
        </div>
      </Tarjeta>

      {mensaje && (
        <div className={`rounded-lg border px-4 py-3 text-sm ${
          mensaje.tipo === "ok" ? "border-green-200 bg-green-50 text-green-700" : "border-red-200 bg-red-50 text-red-700"
        }`}>
          {mensaje.texto}
        </div>
      )}

      <button onClick={guardar} disabled={!puedeGuardar}
        className="w-full sm:w-auto rounded-xl bg-primary-700 px-6 py-3 text-sm font-semibold text-white shadow-md
                   transition hover:bg-primary-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none">
        {loading ? "Guardando…" : "Registrar PQRS"}
      </button>
    </div>
  );
}
""",
    "src/presentation/screens/TableroPage.tsx": """import { useTablero } from "../hooks/useTablero";

function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`glass-card glass-card-interactiva rounded-2xl p-5 ${className}`}>{children}</section>;
}

function TarjetaKPI({ etiqueta, valor, color }: { etiqueta: string; valor: string; color: string }) {
  return (
    <Tarjeta className="flex flex-col gap-1">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{etiqueta}</p>
      <p className="font-mono text-2xl font-bold" style={{ color }}>{valor}</p>
    </Tarjeta>
  );
}

/** Tablero real, Fase 3: lee TODO lo capturado en Firestore (RegistroPeriodo + PQRS) y calcula
 *  los mismos KPIs que el Excel -- Cajas Vigentes, % Avance Global, Unidades Operativas,
 *  Eliminación, Unidades en Riesgo Alto -- mas el desglose por Tarea y por Periodo TRD. */
export function TableroPage() {
  const { resumen, loading, error, refrescar } = useTablero();

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <p className="text-sm text-slate-400">Cargando tablero…</p>
      </div>
    );
  }

  if (error || !resumen) {
    return (
      <Tarjeta className="text-center">
        <p className="text-sm text-red-600">{error || "No se pudo cargar el tablero."}</p>
        <button onClick={refrescar} className="mt-3 text-sm font-semibold text-primary-600 hover:text-primary-700">
          Reintentar
        </button>
      </Tarjeta>
    );
  }

  return (
    <div className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Tablero</p>
          <h1 className="mt-1 text-2xl font-bold text-slate-900">Resumen general</h1>
          <p className="mt-1 text-sm text-slate-500">
            Calculado en vivo con lo capturado hasta ahora — {resumen.unidadesOperativas} unidades operativas.
          </p>
        </div>
        <button onClick={refrescar} className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50">
          ↻ Actualizar
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <TarjetaKPI etiqueta="Cajas Vigentes" valor={String(resumen.cajasVigentesEnSitio)} color="#2563EB" />
        <TarjetaKPI etiqueta="% Avance Global" valor={`${Math.round(resumen.avancePromedioGlobal * 100)}%`} color="#0F766E" />
        <TarjetaKPI etiqueta="Unidades Operativas" valor={String(resumen.unidadesOperativas)} color="#F59E0B" />
        <TarjetaKPI etiqueta="Eliminación (histórico)" valor={String(resumen.cajasEliminacionHistorico)} color="#0F766E" />
        <TarjetaKPI etiqueta="Riesgo Alto" valor={String(resumen.unidadesEnRiesgoAlto)} color="#DC2626" />
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        <Tarjeta>
          <p className="mb-3 text-sm font-semibold text-slate-700">% Avance por Tarea</p>
          <div className="space-y-2.5">
            {resumen.porTarea.map((t) => (
              <div key={t.tarea} className="flex items-center gap-3">
                <span className="w-28 shrink-0 text-xs text-slate-600">{t.tarea}</span>
                <div className="h-2 flex-1 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-primary-500" style={{ width: `${Math.min(t.avancePromedio, 1) * 100}%` }} />
                </div>
                <span className="w-10 shrink-0 text-right font-mono text-xs text-slate-500">{Math.round(t.avancePromedio * 100)}%</span>
              </div>
            ))}
          </div>
        </Tarjeta>

        <Tarjeta>
          <p className="mb-3 text-sm font-semibold text-slate-700">Cajas por Periodo TRD</p>
          <div className="space-y-2.5">
            {resumen.porPeriodo.length === 0 && <p className="text-sm text-slate-400">Sin datos capturados todavía.</p>}
            {resumen.porPeriodo.map((p) => (
              <div key={p.periodo} className="flex items-center justify-between text-sm">
                <span className="text-slate-600">{p.periodo}</span>
                <span className="font-mono font-semibold text-slate-800">{p.totalCajas} cajas · {Math.round(p.avancePromedio * 100)}%</span>
              </div>
            ))}
          </div>
        </Tarjeta>
      </div>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Detalle por Unidad Operativa</p>
        {resumen.porDependenciaServicio.length === 0 ? (
          <p className="text-sm text-slate-400">Aún no hay visitas registradas.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-xs uppercase text-slate-400">
                  <th className="pb-2 pr-4">Unidad</th>
                  <th className="pb-2 pr-4">Cajas Vigentes</th>
                  <th className="pb-2">% Avance</th>
                </tr>
              </thead>
              <tbody>
                {resumen.porDependenciaServicio.map((u) => (
                  <tr key={u.dependencia} className="border-b border-slate-100">
                    <td className="py-2 pr-4 text-slate-700">{u.dependencia}</td>
                    <td className="py-2 pr-4 font-mono text-slate-600">{u.totalCajas}</td>
                    <td className="py-2 font-mono text-slate-600">{Math.round(u.avancePromedio * 100)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Tarjeta>

      <p className="text-center text-xs text-slate-400">
        Actualizado: {new Date(resumen.actualizadoEn).toLocaleString("es-CO")}
      </p>
    </div>
  );
}
""",
    "src/vite-env.d.ts": """/// <reference types="vite/client" />
""",
    "vite.config.ts": """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true
      },
      manifest: {
        name: 'Pérgamo - Gestión Documental',
        short_name: 'Pérgamo',
        description: 'Auditoría de TRD y CCD para unidades operativas',
        theme_color: '#166534',
        background_color: '#FAFAF9',
        display: 'standalone',
        start_url: '/',
        icons: [
          { src: '/pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: '/pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          { src: '/pwa-maskable-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@domain': path.resolve(__dirname, './src/domain'),
      '@application': path.resolve(__dirname, './src/application'),
      '@infrastructure': path.resolve(__dirname, './src/infrastructure'),
      '@presentation': path.resolve(__dirname, './src/presentation')
    }
  }
});""",
}


def main():
    if not os.path.exists("package.json"):
        print("AVISO: corre esto desde la raiz de tu proyecto (donde esta package.json).")
        return
    for ruta, contenido in ARCHIVOS_TEXTO.items():
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        with open(ruta, "w", encoding="utf-8", newline="\n") as f: f.write(contenido)
        print(f"OK  {ruta}  ({len(contenido)} caracteres)")
    print(f"\nListo -- {len(ARCHIVOS_TEXTO)} archivos.")
    print("Corre: npm install")
    print("Despues: reinicia npm run dev y Ctrl+Shift+R")
if __name__ == "__main__": main()
