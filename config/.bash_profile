#export NDK_ROOT=~/soft/android-ndk-r8e
#export PYTHONPATH=~/py_libs
#export PATH=$NDK_ROOT:$PATH

#export PS1="\u@\d:"
#export PS1="\u@\h:\w$ "

export EDITOR="vim"

alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'
alias vi='vim'
alias ls='ls -G'    # mac os x

# alias for java
alias javac='javac -J-Dfile.encoding=UTF-8 -encoding UTF-8'
alias java='java -Dfile.encoding=UTF-8'

#set bell-style none

# Ignore repeated commonds
export HISTCONTROL=ignoredups
# Ignore commonds splited by the colons
export HISTIGNORE="[  ]*:&:bg:fg:exit:ls:rm:pwd"
# Set history file size
export HISTFILESIZE=10000000
# Set the number of commands to remember
export HISTSIZE=1000000
shopt -s histappend
shopt -s checkwinsize
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

# For virtualenv
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
