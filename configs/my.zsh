export PATH=$PATH:$HOME/bin:$HOME/scripts
export EDITOR="vim"

alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'
alias vi='vim'
alias ls='ls -G'    # mac os x

# Ignore repeated commonds
export HISTCONTROL=ignoredups
# Ignore commonds splited by the colons
export HISTIGNORE="[  ]*:&:bg:fg:exit:ls:pwd"
# Set history file size
export HISTFILESIZE=10000000
# Set the number of commands to remember
export HISTSIZE=1000000

# alias for java
alias javac='javac -J-Dfile.encoding=UTF-8 -encoding UTF-8'
alias java='java -Dfile.encoding=UTF-8'

export ANDROID_NDK=$HOME/Library/Android/sdk/ndk-bundle/
export PATH=$ANDROID_NDK:$HOME/Library/Android/sdk/platform-tools:$PATH

# CCACHE
export USE_CCACHE=1
export NDK_CCACHE=/usr/local/bin/ccache

# alias for hidden files
alias hideFiles='defaults write com.apple.finder AppleShowAllFiles NO; killall Finder /System/Library/CoreServices/Finder.app'
alias showFiles='defaults write com.apple.finder AppleShowAllFiles YES; killall Finder /System/Library/CoreServices/Finder.app'

# avoid locale warning messages
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
