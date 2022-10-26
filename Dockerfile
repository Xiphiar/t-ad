FROM ubuntu:20.04

# set working directory
WORKDIR /root/


# update and install packages
RUN apt-get update \
  && apt-get update \
  && apt-get install python3 python3-pip git openssh-client apt-utils curl jq wget -y

# install go
RUN wget https://go.dev/dl/go1.17.6.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.6.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

# copy the iond files
RUN git clone https://github.com/IDEP-network/SanfordV2.git
RUN cp SanfordV2/iond /usr/local/bin/
RUN chmod a+x /usr/local/bin/iond

# install wasmvm
RUN /usr/local/go/bin/go get -u github.com/CosmWasm/wasmvm@v1.0.0-beta4
RUN chmod +x /root/go/pkg/mod/github.com/\!cosm\!wasm/wasmvm@v1.0.0-beta4/api/libwasmvm.so
RUN cp -r $HOME/go/pkg/mod/github.com/\!cosm\!wasm/wasmvm@v1.0.0-beta4/api/libwasmvm.so /usr/lib/

# copy install the requirements
ADD ./tendermint-autodelegation.py /root/
ADD ./requirements.txt /root/
RUN pip3 install -r requirements.txt

# run the script
CMD /usr/local/bin/iond start
