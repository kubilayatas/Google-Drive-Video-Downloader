CoordMode("Pixel", "Screen")
CoordMode("Mouse", "Screen")

; -------- Email Adımı --------
ErrorLevel := 1
if ImageSearch(&posX, &posY, 0, 0, A_ScreenWidth, A_ScreenHeight, "*100 email.png") = 0 {
    Click posX + 1000, posY + 185
    Sleep 500
    Send("kuatas@gelisim.edu.tr")
    Sleep 100
    Send("{Enter}")
    MsgBox("Email girildi")
} else {
    MsgBox("Email görseli bulunamadı.")
}

; -------- Şifre Adımı --------
ErrorLevel := 1
if ImageSearch(&posX, &posY, 0, 0, A_ScreenWidth, A_ScreenHeight, "*100 sifre.png") = 0 {
    Click posX + 1000, posY + 230
    Sleep 500
    Send("*2923*Kubila")
    Sleep 100
    Send("{Enter}")
    MsgBox("Şifre girildi")
} else {
    MsgBox("Şifre görseli bulunamadı.")
}

; -------- Profil Ekle Adımı --------
ErrorLevel := 1
if ImageSearch(&posX, &posY, 0, 0, A_ScreenWidth, A_ScreenHeight, "*100 profile-ekle.png") = 0 {
    Click posX + 50, posY + 540
    Sleep 500
    Send("{Enter}")
    MsgBox("Profil ok")
} else {
    MsgBox("Profil ekle görseli bulunamadı.")
}
