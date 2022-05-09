# Dynascii

DDDDDDDDDDDDD       YYYYYYY       YYYYYYYNNNNNNNN        NNNNNNNN               AAA                 SSSSSSSSSSSSSSS         CCCCCCCCCCCCCIIIIIIIIIIIIIIIIIIII
D::::::::::::DDD    Y:::::Y       Y:::::YN:::::::N       N::::::N              A:::A              SS:::::::::::::::S     CCC::::::::::::CI::::::::II::::::::I
D:::::::::::::::DD  Y:::::Y       Y:::::YN::::::::N      N::::::N             A:::::A            S:::::SSSSSS::::::S   CC:::::::::::::::CI::::::::II::::::::I
DDD:::::DDDDD:::::D Y::::::Y     Y::::::YN:::::::::N     N::::::N            A:::::::A           S:::::S     SSSSSSS  C:::::CCCCCCCC::::CII::::::IIII::::::II
  D:::::D    D:::::DYYY:::::Y   Y:::::YYYN::::::::::N    N::::::N           A:::::::::A          S:::::S             C:::::C       CCCCCC  I::::I    I::::I  
  D:::::D     D:::::D  Y:::::Y Y:::::Y   N:::::::::::N   N::::::N          A:::::A:::::A         S:::::S            C:::::C                I::::I    I::::I  
  D:::::D     D:::::D   Y:::::Y:::::Y    N:::::::N::::N  N::::::N         A:::::A A:::::A         S::::SSSS         C:::::C                I::::I    I::::I  
  D:::::D     D:::::D    Y:::::::::Y     N::::::N N::::N N::::::N        A:::::A   A:::::A         SS::::::SSSSS    C:::::C                I::::I    I::::I  
  D:::::D     D:::::D     Y:::::::Y      N::::::N  N::::N:::::::N       A:::::A     A:::::A          SSS::::::::SS  C:::::C                I::::I    I::::I  
  D:::::D     D:::::D      Y:::::Y       N::::::N   N:::::::::::N      A:::::AAAAAAAAA:::::A            SSSSSS::::S C:::::C                I::::I    I::::I  
  D:::::D     D:::::D      Y:::::Y       N::::::N    N::::::::::N     A:::::::::::::::::::::A                S:::::SC:::::C                I::::I    I::::I  
  D:::::D    D:::::D       Y:::::Y       N::::::N     N:::::::::N    A:::::AAAAAAAAAAAAA:::::A               S:::::S C:::::C       CCCCCC  I::::I    I::::I  
DDD:::::DDDDD:::::D        Y:::::Y       N::::::N      N::::::::N   A:::::A             A:::::A  SSSSSSS     S:::::S  C:::::CCCCCCCC::::CII::::::IIII::::::II
D:::::::::::::::DD      YYYY:::::YYYY    N::::::N       N:::::::N  A:::::A               A:::::A S::::::SSSSSS:::::S   CC:::::::::::::::CI::::::::II::::::::I
D::::::::::::DDD        Y:::::::::::Y    N::::::N        N::::::N A:::::A                 A:::::AS:::::::::::::::SS      CCC::::::::::::CI::::::::II::::::::I
DDDDDDDDDDDDD           YYYYYYYYYYYYY    NNNNNNNN         NNNNNNNAAAAAAA                   AAAAAAASSSSSSSSSSSSSSS           CCCCCCCCCCCCCIIIIIIIIIIIIIIIIIIII

## What it is?

Dynascii is a light-weighted utility or application to casting things to Telnet. It is implemented in Python and aimed to deploy quickly and easily on a server with a proper environment.

## Can I have a preview?

Demos can be found at [_telnet dynascii.tarcadia.site 6023_](telnet://dynascii.tarcadia.site:6023) for Still Alive and at [_telnet dynascii.tarcadia.site 6024_](telnet://dynascii.tarcadia.site:6024) for Bad Apple.

## How it comes?

Dynascii is an idea rooted in two things, that i. my willing to make a light-weighted, old-school web service and ii. errorer's super eye-catching video of playing Still Alive on an EL terminal [用80年代EL显示屏终端机播放《传送门》主题曲Still Alive](https://www.bilibili.com/video/BV1cU4y1A7ud). I was working on telnet protocols that time and when errorer published this video I suddenly realized that it may not be necessary to make a BBS or something like that. A telnet video stream that sparks you with a 1900s wind could satisfy me and many other people, and anyone who can access this stream can feel the joy of rediscovering history. An early version of the prototype of Dynascii can be found in [Tarcadia/Telnet-Cast-Portal_StillAlive](https://github.com/Tarcadia/Telnet-Cast-Portal_StillAlive), as a fork from [errorer/Portal_StillAlive_Python](https://github.com/errorer/Portal_StillAlive_Python).

## How it is designed?

This project is designed to be a small project, that any unnecessary codes and unnecessary intern relations should be avoided. So the projet codes are separately organized. Parameters are used to set properties for the main file, and it use informal imports which can be propertied by input parameters to access implementations which are separate files.

These implementations may cause some difficulty to read the code and to debug. But it provides a super flexibility to add components and reconfiguration the deployed application. By ensuring the stabiliy of these several lines of codes, I think this is a most balanced position between project managment, code reliability, and deployment flexibility.

## How to use?

Run the _badapple.sh_ or _stillalive.sh_ to start a server, where all configs can be found and modified.
