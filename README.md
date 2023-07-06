
# Client cached content decompiler
This script is extracting client build from ss14 sqlite database with cached servers (content.db).




## Usage

```bash
  git clone https://github.com/freeze2222/ss14_client_decompiler
  pip install zstandard
```
Move content.db to the same folder as script (content.db is located at windows in %AppData%\..\Local\Space Station 14\launcher)
```
python ./main.py
```
It will list all avalible fork ids, you should choose one of them. Data folder will be created with all client files in sctipt directory. To decompile C# code you can use 
[dnSpy](https://github.com/dnSpy/dnSpy/releases/tag/v6.1.8) or other decompilers.
    
## Disclaimer 
I am not responsible for any abuse or damage caused by this program. Only for testing purposes.