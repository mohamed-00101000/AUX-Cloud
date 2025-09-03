#!/C:/Users/popma/bin/tclsh
# /c/Users/popma/bin/tclsh  "e:\Shared Folders\Uni\Racing team\Final\cloud codes\run.tcl" # on get bash shell
# Define full Python executable path first
set python3 "C://Users//popma//AppData//Local//Programs//Python//Python313//python.exe"
puts "Setting parameters"
# Set parameters
set send_base_url "https://racingteam.rf.gd/new/add.php"
set send_delay 2

set get_base_url "http://racingteam.rf.gd/new/data.json"
set get_delay 1
puts "Running python files"
# Run both scripts using the defined python3 variable - http
puts "Running automaticsendtesting - http"
exec $python3 automaticsendtesting.py $send_base_url $send_delay &
puts "Running automaticgettesting - http"
exec $python3 automaticgettesting.py $get_base_url $get_delay &
# Run both scripts using the defined python3 variable - ftp
puts "Running sendftp - ftp"
exec $python3 sendftp.py $send_base_url $send_delay &
puts "Running getftp - ftp"
exec $python3 getftp.py $get_base_url $get_delay &
puts "Running sendftp_station - ftp"
exec $python3 sendftp_station.py $get_base_url $get_delay &
