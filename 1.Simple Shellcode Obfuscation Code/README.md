# Simple ShellCode Obfuscation Script

```
๐จ โบโบโบ python ssos.py

      โโโโโโโโโ  .dMMMb  .dMMMb  .aMMMb  .dMMMb
 โ  โโโโโโโโโโ  dMP" VP dMP" VP dMP"dMP dMP" VP
  โโโโโโโโโโโ   VMMMb   VMMMb  dMP dMP  VMMMb
  โโโโโโโโโโ  dP .dMP dP .dMP dMP.aMP dP .dMP
 โโโโโโโโโโ   VMMMP"  VMMMP"  VMMMP"  VMMMP"

 Simple ShellCode Obfuscation Script v1.0
 https://github.com/inspiringz/python-toys @3ND

[+] Usage: python sscs.py payload.py output_filename
   - For ps1: powershell -ExecutionPolicy bypass -File exploit.ps1
   - For xml: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe exploit.xml

[+] Been Test On: <2021/07/15>
   - ็ซ็ป๏ผ็ๆฌ 5.0.62.3 / ็ๆฏๅบ 2021-07-12๏ผ-> ps1, xml works well
   - 360๏ผ็ๆฌ 13.1.0.1002 / ๅค็จๆจ้ฉฌๅบ 2021-07-15๏ผ-> ps1, xml works well
   - ๅกๅทดๆฏๅบ๏ผ็ๆฌ 21.3.10.391b๏ผ-> ps1, xml works well
   - Defender (ๅฎขๆท็ซฏ็ๆฌ: 4.18.2106.6 / ๅผๆ็ๆฌ: 1.1.18300.4 / ้ฒ็ๆฏ่ฝฏไปถ็ๆฌ: 1.343.1035.0) -> ps1, xml works

[+] Suggest: Use Malleable C2 Profile For CobaltStrike
```

## Usage

Step 1:

![](images/16263526414680.jpg)

![](images/16263526638086.jpg)

![](images/16263526763907.jpg)


Step 2:


```
โฏ python sscs.py payload.py exploit

      โโโโโโโโโ  .dMMMb  .dMMMb  .aMMMb  .dMMMb
 โ  โโโโโโโโโโ  dMP" VP dMP" VP dMP"VMP dMP" VP
  โโโโโโโโโโโ  VMMMb   VMMMb  dMP      VMMMb
  โโโโโโโโโโ  dP .dMP dP .dMP dMP.aMP dP .dMP
 โโโโโโโโโโ   VMMMP"  VMMMP"  VMMMP"  VMMMP"

 Simple ShellCode Confuse Script v1.0 By 3ND


[+] >>>> Powershell Script Generated to exploit.ps1
[+] Usage: powershell -ExecutionPolicy bypass -File exploit.ps1

[+] >>>> Xml Script Generated to exploit.xml
[+] Usage: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe exploit.xml
```

![](images/shelp.png)


Step 3:

ps1:

```bash
powershell -ExecutionPolicy bypass -File exploit.ps1
```

![](images/ps1.png)

![](images/ps1x.png)


or xml:

```bash
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe exploit.xml
```

![](images/ka.png)


![](images/xml.png)