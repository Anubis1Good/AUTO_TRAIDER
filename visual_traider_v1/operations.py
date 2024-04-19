from traid_utils import click_bid, click_close, reset_bid, reset_close
def send_bid(region):
    click_bid(region)

def has_bid(region):
    reset_bid(region)

def need_close(region):
    click_close(region)

def has_close(region):
    reset_close(region)