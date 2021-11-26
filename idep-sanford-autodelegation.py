#!/usr/bin/env python3
import os, requests
import configparser
from subprocess import Popen, PIPE

class IdepAutodelegation():
    def __init__( self, config_file='config.ini' ):
        # obtain the host name
        self.name = os.uname()[1]

        # read the config and setup the telegram
        self.read_config( config_file )
        self.setup_telegram()
        self.setup_idep_info()

        # send the hello message
        self.send( f'{self.name}: Hello from IDEP Autodelegation Bot!' )

        # obtain the balance
        response = self.get_balance( )
        print( response )
        
    def read_config( self, config_file ):
        '''
        Read the configuration file
        '''
        config = configparser.ConfigParser()
        config.read( config_file )
        self.config = config

    def setup_telegram( self ):
        '''
        Setup telegram
        '''
        self.telegram_token = self.config['Telegram']['telegram_token']
        self.telegram_chat_id = self.config['Telegram']['telegram_chat_id']

    def setup_idep_info( self ):
        '''
        Setup idep info
        '''
        self.chain_id = self.config['IDEP']['chain_id']
        self.wallet_name = self.config['IDEP']['wallet_name']
        self.wallet_key = self.config['IDEP']['wallet_key']
        self.validator_key = self.config['IDEP']['validator_key']

    def send( self, msg ):
        '''
        Send telegram message
        '''
        requests.post( f'https://api.telegram.org/bot{self.telegram_token}/sendMessage?chat_id={self.telegram_chat_id}&text={msg}' )

    def get_balance( self ):
        '''
        Obtain the IDEP balance
        '''
        return os.system( f'iond q bank balances { self.wallet_key }' )

    def distribute_rewards( self ):
        '''
        Distribute the rewards from the validator
        '''
        return os.system( f'iond tx distribution withdraw-rewards { self.validator_key } --chain-id={ self.chain_id } --from {self.wallet_name}' )

    def delegate( self, amount, delegate ):
        '''
        Distribute the rewards from the validator
        '''
        return os.system( f'iond tx staking delegate { delegate } { amount }idep --from { self.wallet_name } --chain-id { self.chain_id }' )
    
idep_bot = IdepAutodelegation()
