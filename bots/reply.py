import os, datetime

import discord
from discord.ext import commands

from .helper import STUD_FILE

SERVER = {}

prefix = '>'

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')
commands = ['help','reply']
usage = {
  'help': '`>help`',
  'reply': '`>_messageID_` _reply_'
}

''' Events '''

@bot.event
async def on_ready():
  act = discord.Activity()
  act.type = discord.ActivityType.watching
  act.name = 'your messages'
  await bot.change_presence(activity=act)
  print("konichiwa minasan")

@bot.event
async def on_message(msg):
  ctx = await bot.get_context(msg)
  if not ctx.valid and ctx.prefix == prefix: await ctx.invoke(reply)
  elif ctx.command: await ctx.invoke(ctx.command)


''' Commands '''

@bot.command(pass_context=True)
async def help(ctx, *args):
  if len(args)!=0: await ctx.message.channel.send('Usage: `>help` ')
  else:
    em = discord.Embed(
      title='Usage Instructions',
      description='Use this bot to reply to messages',
      color=0xCDDC96
    )
    em.set_author(name='[bot] reply-beta')
    em.add_field(name='Commands', value=', '.join(commands), inline=False)
    for command in commands:
      em.add_field(name=command, value=usage[command])
    await ctx.message.channel.send(embed=em)

@bot.command(pass_context=True)
async def reply(ctx, *args):
  reply_to_id = ctx.message.content.split()[0][1:]; em = None
  try: 
    reply_to = await ctx.message.channel.fetch_message(reply_to_id)
    em = create_embed(reply_to, ctx.message)
  except discord.NotFound: 
    await ctx.message.channel.send('Message ID: {0} not found in channel'.format(reply_to_id))
    await ctx.invoke(help)
  except discord.Forbidden: 
    await ctx.message.channel.send('I do not have access to the message being referred to!')
  await ctx.message.channel.send(embed=em)


''' Helpers '''

def create_embed(reply_to, reply):

  reply_msg = ' '.join(reply.clean_content.split(' ')[1:])
  embeds = reply_to.embeds
  attached = reply_to.attachments

  em = discord.Embed()
  em.title = ':point_up_2: {0.author.display_name}\'s message is a reply to {1.author.display_name} :point_down:'.format(reply,reply_to)
  em.color = 0x44BFC1
  em.timestamp = reply.created_at

  if (not attached and reply_msg and reply_to.clean_content
      or not attached and not embeds and reply_msg): em.add_field(name='Original Message',value='[{0.clean_content}]({0.jump_url})'.format(reply_to),inline=False)
  elif not attached and reply_msg: em.add_field(name='Original Message',value='[Embedded content]({0.jump_url})'.format(reply_to),inline=False)
  elif reply_msg:
    em.add_field(name='Original Message',value='[Embedded content]({0.jump_url})'.format(reply_to),inline=False)
    for ext in ['.jpg','.jpeg','.png','.gif']:
      if attached[0].url.endswith(ext): em.set_image(url=attached[0].url); break
    else:
      for f in attached: em.add_field(name='Attached file', value='{0.url}'.format(f))
  em.add_field(name='Reply',value='[{0}]({1.jump_url})'.format(reply_msg,reply),inline=False)
  em.set_footer(text='Click the links to jump to the messages')
  return em

async def run_command(command):
  if not os.environ.get('BU_MGMT'): exit('token not found')
  bot.run(os.environ['BU_MGMT'])
  if command not in bot.commands: return False

  await bot.logout()
  return True
  
if __name__=='__main__':
  if not os.environ.get('BUHACK_GIFT'): exit('token not found')
  bot.run(os.environ['BUHACK_GIFT'])
