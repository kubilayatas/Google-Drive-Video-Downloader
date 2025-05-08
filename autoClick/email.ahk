WinActivate("Google Drive: Oturum Açın - Google Chrome")  ; Pencere başlığına göre bulur
WinActivate("Google Drive: Oturum Açın - Google Chrome")
CoordMode("Pixel", "Window")
CoordMode("Mouse", "Window")

; Pencere içi ölçüleri al
WinGetClientPos(&x, &y, &w, &h, "Google Drive: Oturum Açın - Google Chrome")

; -------- Email Adımı --------
    Click x +1080, y +460
    Sleep 1000
    Send("kuatas@gelisim.edu.tr")
    Sleep 1000
    Send("{Enter}")
	Sleep 5000
; -------- Şifre Adımı --------
    ;Click x +1180, y +525
    ;Sleep 1000
    Send("*2923*Kubila")
    ;Sleep 1000
    Send("{Enter}")
	Sleep 10000
; -------- profil Adımı --------
;WinGetClientPos(&x, &y, &w, &h, "")
    Click 50, 540
    Sleep 1000
    Click 384, 590