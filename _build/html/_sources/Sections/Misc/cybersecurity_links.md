
# Cybersecurity Online Resources

## YouTube Channels

### Pentester Academy
Pentester Academy, contributed to and run in collaboration by the same excellent instructor from SecurityTube, this site has many courses available pertinent to pentesting and computer security.  
[Pentester Academy Youtube Channel](https://www.youtube.com/channel/UChjC1q6Ami7W0E71TzPZELA)

---

### Open Security Training
Open Security Training has excellent courses in the field of computer security.  
[Open Security Training Youtube Channel](https://www.youtube.com/user/OpenSecurityTraining)

---

### SecurityTube
The Security Tube is an excellent resource for learning computer security and ethical hacking.  
[The Security Tube Youtube Channel](https://www.youtube.com/user/TheSecurityTube)

---

### Hackersploit
Hackersploit, first name Alexis, is a really good computer security / ethical hacking instructor. He has an excellent Youtube channel and private website.  
[Hackersploit's Youtube Channel](https://www.youtube.com/channel/UC0ZTPkdxlAKf-V33tqXwi3Q/featured)  
[Capture The Flag (CTF) Series](https://www.youtube.com/playlist?list=PLBf0hzazHTGOyRReqMyE-CDMWAQ5AgXO-)

---

### IppSec
Excellent video tutorials on hacking, Capture The Flag (CTF), and Hack The Box.  
[IppSec's Youtube Channel](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA)  
[IppSec's Playlists](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA/playlists)

---

### Joseph Delgadillo
Joseph Delgadillo offers a Complete Ethical Hacking Course, beginner to advanced.  
[The Complete Ethical Hacking Course: Beginner to Advanced!](https://www.youtube.com/watch?v=vg9cNFPQFqM)

---

### NetSecNow (www.PentesterUniversity.org)
Full of many great videos on computer security / ethical hacking.  
[How-to Penetration Testing and Exploiting with Metasploit + Armitage + msfconsole](https://www.youtube.com/watch?v=lZlqr2PFJIo&t=2414s)  
[NetSecNow's Main Youtube Channel](https://www.youtube.com/channel/UC6J_GnSAi7F2hY4RmnMcWJw)

---

### MIT Open Courseware
MIT 6.858 Computer Systems Security, Fall 2014  
[Click here for youtube videos from course](https://www.youtube.com/watch?v=yRVZPvHYHzw&index=9&list=PLUl4u3cNGP62K2DjQLRxDNRi0z2IRWnNh)

---

## Websites

### NetSecNow (www.PentesterUniversity.org)
[Pentester University's website (paid)](https://www.pentesteruniversity.org/)

---

### Pentester Academy (Free and Paid)
This site is full of excellent computer security / ethical hacking courses. You can even get certifications.  
[Pentester Academy (Free and Paid)](https://www.pentesteracademy.com/)

---

### Open Security Training (Free)
Excellent courses on ARM and x86 Assembly, Binaries, Exploits and Malware  
[Open Security Training (Free)](http://www.opensecuritytraining.info/)  
[Hacking Techniques and Intrusion Detection](http://opensecuritytraining.info/HTID.html)

---

### SecurityTube (paid)
This site is full of excellent computer security / ethical hacking courses. You can even get certifications.  
[Security Tube's Training Site (paid)](http://www.securitytube-training.com/)

---

### MIT Open Courseware
MIT 6.858 Computer Systems Security, Fall 2014  
Instructor: Armando Solar-Lezama  
[Click here for course](http://ocw.mit.edu/6-858F14)

---

### Azeria Labs ARM Assembly and Shellcoding Techniques
[INTRODUCTION TO WRITING ARM SHELLCODE](https://azeria-labs.com/writing-arm-shellcode/)

---

### Smashing The Stack For Fun And Profit
by Aleph One  
[Smashing the Stack For Fun and Profit](https://insecure.org/stf/smashstack.html)

---

## Mastering Gnu DeBugger (GDB)

### Modular Visual Interfaces for GDB

#### GEF - GDB Enhanced Features for exploit devs and reversers
:::{image} images/gef_screenshot.png
:alt: GEF Screenshot
:align: center
:::
 
[GEF - GDB Enhanced Features for exploit devs and reversers](https://github.com/hugsy/gef)

---

#### GDB Dashboard (Modular, Terminal Based Color UI)
![GDB Dashboard Screenshot](images/gdb_dashboard_screenshot.png)  
[Modular visual interface for GDB in Python](https://github.com/cyrus-and/gdb-dashboard)

---

#### PEDA - Python Exploit Development Assistance for GDB
![PEDA Screenshot](images/peda_screenshot.png)  
[Python Exploit Development Assistance](https://github.com/longld/peda)

---

#### GDB Dashboard by cyrus-and
[GDB Dashboard](https://github.com/cyrus-and/gdb-dashboard)

---

#### GDB Grab Bag of Useful Websites and Information

- [GDB commands by function - simple guide](http://web.cecs.pdx.edu/~jrb/cs201/lectures/handouts/gdbcomm.txt)
- [GDB Registers - GDB Manual](https://ftp.gnu.org/old-gnu/Manuals/gdb-5.1.1/html_node/gdb_60.html)
- [4.2 Starting your Program- GDB Manual](https://www-zeuthen.desy.de/unix/unixguide/infohtml/gdb/Starting.html)
- [Choosing modes - GDB Manual](https://ftp.gnu.org/old-gnu/Manuals/gdb/html_node/gdb_8.html#SEC9)
- [10.1 Expressions - GDB Manual](https://sourceware.org/gdb/current/onlinedocs/gdb/Expressions.html#Expressions)

---

Passing a command to GDB when running a program  
set args "`perl -e 'print "A"x20;'`"  
or  
(gdb)run `$(perl -e 'print "A"x20')`  
[Passing a command to GDB when running a program.](https://stackoverflow.com/questions/1070276/passing-a-command-to-gdb-when-running-a-program)

---

Writing memory with GDB  
set *((unsigned char *) 0x1234567) = 50  
[Writing memory with GDB.](https://www.embeddedrelated.com/showthread/comp.arch.embedded/24944-1.php)

---

GDB QUICK REFERENCE GDB Version 4 Essential Commands  
[GDB QUICK REFERENCE GDB Version 4 Essential Commands](http://users.ece.utexas.edu/~adnan/gdb-refcard.pdf)

---

GDB Cheat Sheet  
[GDB Cheat Sheet](https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf)
```

This Markdown format replicates the structure and content of your HTML while converting it to Markdown syntax. If you need to adjust any parts or add more details, let me know!