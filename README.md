# ==Dynascii==

## Happy Birthday Dynascii :tada::tada::tada:

Let's celebrate the birth of Dynascii for 1 Year. :tada::tada::tada:

The prototype of Dynascii was brought out on 12th November 2021 (UTC+8).
I still remember that afternoon, errorer's [StillAlive on EL screen](https://www.bilibili.com/video/BV1cU4y1A7ud) shocked me, and I decided this is what I want to make online.
And after an afternoon, the [beginning version](https://github.com/Tarcadia/Telnet-Cast-Portal_StillAlive) came out.
Later after the dinner, I started building an environment to move it onto the internet.
At midnight 13th November, around 1.30 am or 3.00 am (UTC+8) that I cannot remember, Still Alive is online.
After two days I realized this could be a better project, so I started Dynascii project and placed Bad Apple together with Still Alive from errorer.

So, 16th November 2021 (UTC+8) is the birth of Dynascii because it is formally online with the functions, and today is the 368th day of Dynascii.
During all the days, Dynascii never down even though there are DoS attacks and other burdens.

## What it is?

Dynascii is a light-weighted utility or application to casting things to a stream. It is implemented in Python and aimed to deploy quickly and easily on a server with a proper environment.

## Can I have a preview?

Demos can be found at [_telnet dynascii.tarcadia.net 6023_](telnet://dynascii.tarcadia.net:6023) for Still Alive and at [_telnet dynascii.tarcadia.net 6024_](telnet://dynascii.tarcadia.net:6024) for Bad Apple.

## How it comes?

Dynascii is an idea rooted in two things, that i. my willing to make a light-weighted, old-school web service and ii. errorer's super eye-catching video of playing Still Alive on an EL terminal [用80年代EL显示屏终端机播放《传送门》主题曲Still Alive](https://www.bilibili.com/video/BV1cU4y1A7ud). I was working on telnet protocols that time and when errorer published this video I suddenly realized that it may not be necessary to make a BBS or something like that. A telnet video stream that sparks you with a 1900s wind could satisfy me and many other people, and anyone who can access this stream can feel the joy of rediscovering history. An early version of the prototype of Dynascii can be found in [Tarcadia/Telnet-Cast-Portal_StillAlive](https://github.com/Tarcadia/Telnet-Cast-Portal_StillAlive), as a fork from [errorer/Portal_StillAlive_Python](https://github.com/errorer/Portal_StillAlive_Python).m Use of code is authorised by errorer.

## How it is designed?

This project is designed to be a small project, that any unnecessary codes and unnecessary intern relations should be avoided. So the projet codes are separately organized. Parameters are used to set properties for the main file, and it use informal imports which can be propertied by input parameters to access implementations which are separate files.

These implementations may cause some difficulty to read the code and to debug. But it provides a super flexibility to add components and reconfiguration the deployed application. By ensuring the stabiliy of these several lines of codes, I think this is a most balanced position between project managment, code reliability, and deployment flexibility.

## How to use?

Check for the repository [Dynascii](https://github.com/Tarcadia/Dynascii). Run the _demo/badapple.sh_ or _demo/stillalive.sh_ to start a server, where most configs can be found and modified.

Use python3 -m dynascii --help_ for help, and there are listed helps below:

- --log log_file                : str, path to log file
- --log-level log_level = INFO  : str, name of logging level
- -6                            : flag, use of IPv6
- --host host                   : str, hostname of server
- --port port = 23              : uint16, port of server
- --blocking-io                 : flag, use of blocking IO
- --no-blocking-io              : flag, use of blocking IO, flagged for not using
- --blocking-timeout blocking_timeout = 3   : uint, time of blocking IO timeout, 0 for no timeout
- --no-blocking-delay no_blocking_delay = 1 : uint, time of non-blocking IO inter-polling delay
- --backlogs backlogs = 16                  : uint, backlogs of server
- --poolsize pool_size = 32                 : uint, size of server thread pool
- --shell shell = nullshell                 : module, name of shell module
- -- --xxx xxx --yyy yyy                    : extra params for shell
