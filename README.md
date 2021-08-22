# sms-report

## 着信したSMSを読み出してGoogle SpreadSheetへ書き出すスクリプト

USBドングル  
HUAWEI E8372h-155

ラズパイにUSBドングルを認識させるために  
/etc/usb_modeswitch.conf  
で  
HuaweiAltModeGlobal=1  
を設定する。

Google SpreadSheetへのアクセスに必要なモジュールをインストールする。  
$ pip install --upgrade google-api-python-client  
$ pip install --upgrade oauth2client  

スクリプトをバックグラウンドで起動する。  
$ nohup sh sms.sh &  
