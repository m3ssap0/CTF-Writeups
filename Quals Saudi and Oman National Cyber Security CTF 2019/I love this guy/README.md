# Quals Saudi and Oman National Cyber Security CTF 2019 – I love this guy

* **Category:** Malware Reverse Engineering
* **Points:** 100

## Challenge

> Can you find the password to obtain the flag?
>
> [https://s3-eu-west-1.amazonaws.com/hubchallenges/Reverse/ScrambledEgg.exe](https://s3-eu-west-1.amazonaws.com/hubchallenges/Reverse/ScrambledEgg.exe)

## Solution

The challenge gives you a .NET executable file: [ScrambledEgg.exe](ScrambledEgg.exe).

Reversing the application with *JetBrains dotPeek* and analyzing the `MainWindow` component will lead to the following code.

```c#
...

public char[] Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_".ToCharArray();

...

private void Button_Click(object sender, RoutedEventArgs e)
{
  if (!this.TextBox1.Text.Equals(new string(new char[5]
  {
    this.Letters[5],
    this.Letters[14],
    this.Letters[13],
    this.Letters[25],
    this.Letters[24]
  })))
    return;
  int num = (int) MessageBox.Show(new string(new char[18]
  {
    this.Letters[5],
    this.Letters[11],
    this.Letters[0],
    this.Letters[6],
    this.Letters[26],
    this.Letters[8],
    this.Letters[28],
    this.Letters[11],
    this.Letters[14],
    this.Letters[21],
    this.Letters[4],
    this.Letters[28],
    this.Letters[5],
    this.Letters[14],
    this.Letters[13],
    this.Letters[25],
    this.Letters[24],
    this.Letters[27]
  }));
}

...
```

The following C# code could be used to reverse password and flag.

```c#
using System;

class MainClass {
  public static void Main (string[] args) {
    
    char[] Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_".ToCharArray();

    string password = "" + Letters[5] + Letters[14] + Letters[13] + Letters[25] + Letters[24];
    Console.WriteLine ("Password : " + password);

    string flag = "" + Letters[5] + Letters[11] + Letters[0] + Letters[6] + Letters[26] + Letters[8] + Letters[28] + Letters[11] + Letters[14] + Letters[21] + Letters[4] + Letters[28] + Letters[5] + Letters[14] + Letters[13] + Letters[25] + Letters[24] + Letters[27];
    Console.WriteLine ("Flag     : " + flag);
  }
}
```

The password is: `FONZY`.

The flag is: `FLAG{I_LOVE_FONZY}`.