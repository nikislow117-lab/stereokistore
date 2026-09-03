import discord
from discord.ext import commands, tasks
import os
import random
import time
from datetime import datetime

# DEBUG: Check environment variables (REMOVE AFTER IT WORKS)
print("=" * 50)
print("🔍 CHECKING ENVIRONMENT VARIABLES:")
print("=" * 50)
print(f"DISCORD_TOKEN exists: {os.getenv('DISCORD_TOKEN') is not None}")
token = os.getenv('DISCORD_TOKEN')
if token:
    print(f"DISCORD_TOKEN length: {len(token)} characters")
    print(f"DISCORD_TOKEN starts with: {token[:10]}...")
else:
    print("❌ DISCORD_TOKEN is EMPTY or None!")
print(f"CHANNEL_ID: {os.getenv('CHANNEL_ID')}")
print("=" * 50)

# Get token from environment
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 0))

# Validate token
if not TOKEN:
    print("❌ FATAL: DISCORD_TOKEN not found in environment variables!")
    print("Please add DISCORD_TOKEN to your environment variables.")
    exit(1)

if len(TOKEN) < 20:
    print(f"❌ FATAL: DISCORD_TOKEN is too short ({len(TOKEN)} chars)")
    print("A valid Discord token should be 60+ characters.")
    exit(1)

print(f"✅ Token validated! Length: {len(TOKEN)} characters")

if CHANNEL_ID == 0:
    print("⚠️ WARNING: CHANNEL_ID not set or invalid!")
    print("Please add CHANNEL_ID to your environment variables.")

# Bot setup with proper intents
intents = discord.Intents.default()
intents.message_content = True  # Required for commands
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None  # Disable default help command
)

class TransactionBot(commands.Cog):
    """IGitems style transaction bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.order_counter = 480000
        self.avatar_url = "https://i.imgur.com/axv2qqm.png"
        self.banner_url = "https://i.imgur.com/CewEePA.png"
        self.transaction_history = []
        self.post_transaction.start()
        print("✅ TransactionBot cog initialized")

    def cog_unload(self):
        self.post_transaction.cancel()
        print("🛑 TransactionBot cog unloaded")

    def generate_transaction(self):
        """Generate a realistic transaction"""
        self.order_counter += 1
        
        # Payment methods with emojis
        payment_methods = {
            'Dogecoin': {'emoji': '🐕', 'color': 0xC2A633},
            'Bitcoin': {'emoji': '₿', 'color': 0xF7931A},
            'Ethereum': {'emoji': '⟠', 'color': 0x627EEA},
            'Litecoin': {'emoji': 'Ł', 'color': 0x345D9D},
            'Solana': {'emoji': '◎', 'color': 0x9945FF},
            'USDC': {'emoji': '💎', 'color': 0x2775CA},
            'Tether': {'emoji': '₮', 'color': 0x26A17B},
            'Cardano': {'emoji': '₳', 'color': 0x0033AD},
            'Monero': {'emoji': 'ɱ', 'color': 0xFF6600},
            'BNB': {'emoji': '🟡', 'color': 0xF3BA2F}
        }
        
        payment_method = random.choice(list(payment_methods.keys()))
        method_data = payment_methods[payment_method]
        
        # Random amount (weighted)
        if random.random() < 0.2:
            amount = round(random.uniform(500, 5000), 2)  # Big transaction
        elif random.random() < 0.4:
            amount = round(random.uniform(200, 499), 2)   # Medium transaction
        else:
            amount = round(random.uniform(50, 199), 2)    # Small transaction
        
        # Generate transaction hash
        tx_hash = ''.join(random.choices('0123456789abcdef', k=64))
        formatted_hash = f"{tx_hash[:20]}...{tx_hash[-20:]}"
        
        # Random confirmations
        confirmations = random.randint(10, 200)
        
        # Rating (mostly 5 stars)
        rating = random.choices([5, 4, 5, 5, 5, 5, 5], weights=[60, 5, 10, 10, 5, 5, 5])[0]
        
        # Generate order ID
        order_id = f"IG-{''.join(random.choices('0123456789ABCDEF', k=10))}"
        
        # Status (mostly completed)
        status = random.choices(['Completed', 'Completed', 'Completed', 'Processing', 'Completed'])[0]
        
        # Current time
        current_time = datetime.now().strftime('%m/%d/%y, %I:%M %p')
        
        # Trader names
        traders = [
            'CryptoWhale🐋', 'MoonTrader🌙', 'DiamondHands💎', 
            'PandaTrades🐼', 'FoxTrader🦊', 'WolfPack🐺',
            'PhoenixRising🔥', 'DragonTrader🐉', 'HodlKing👑'
        ]
        
        return {
            'order_number': self.order_counter,
            'payment_method': payment_method,
            'emoji': method_data['emoji'],
            'color': method_data['color'],
            'deal_amount': amount,
            'rating': rating,
            'order_id': order_id,
            'transaction_hash': formatted_hash,
            'full_hash': tx_hash,
            'confirmations': confirmations,
            'time': current_time,
            'status': status,
            'trader': random.choice(traders),
            'network_fee': round(random.uniform(0.01, 5), 3)
        }

    @tasks.loop(seconds=120)
    async def post_transaction(self):
        """Post a transaction every 2 minutes"""
        try:
            channel = self.bot.get_channel(CHANNEL_ID)
            if not channel:
                print(f"❌ Channel {CHANNEL_ID} not found!")
                return

            # Generate transaction
            tx = self.generate_transaction()
            
            # Create premium embed
            embed = discord.Embed(
                title="🟢 **IGitems Transactions Bot**",
                description="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                color=tx['color'],
                timestamp=datetime.now()
            )
            
            # Set images
            embed.set_thumbnail(url=self.avatar_url)
            embed.set_image(url=self.banner_url)
            
            # Transaction Status
            status_emoji = "✅" if tx['status'] == "Completed" else "⏳"
            embed.add_field(
                name="\u200b",
                value=f"{status_emoji} **Transaction {tx['status']}**",
                inline=False
            )
            
            # Order Header
            embed.add_field(
                name="\u200b",
                value=f"📋 **Order #{tx['order_number']:,}**",
                inline=False
            )
            
            # Payment Method
            embed.add_field(
                name="💳 **Payment Method**",
                value=f"{tx['emoji']} **{tx['payment_method']}**",
                inline=True
            )
            
            # Deal Amount
            embed.add_field(
                name="💰 **Deal Amount**",
                value=f"**${tx['deal_amount']:,.2f}** USD",
                inline=True
            )
            
            # Rating
            stars = "⭐" * tx['rating'] + "☆" * (5 - tx['rating'])
            embed.add_field(
                name="🏆 **Trader Rating**",
                value=f"{stars}\n**{tx['rating']}/5**",
                inline=True
            )
            
            # Trader (Hidden)
            embed.add_field(
                name="👤 **Trader**",
                value=f"**{tx['trader']}** *(Hidden)*",
                inline=True
            )
            
            # Order ID
            embed.add_field(
                name="🔖 **Order ID**",
                value=f"`{tx['order_id']}`",
                inline=True
            )
            
            # Blockchain
            embed.add_field(
                name="⛓️ **Blockchain**",
                value=f"**{tx['payment_method']}**",
                inline=True
            )
            
            # Separator
            embed.add_field(
                name="\u200b",
                value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                inline=False
            )
            
            # Transaction Hash
            embed.add_field(
                name="🔗 **Transaction Hash**",
                value=f"```\n{tx['transaction_hash']}\n```",
                inline=False
            )
            
            # Confirmations with progress bar
            bar_length = min(tx['confirmations'] // 10, 10)
            conf_bar = "🟩" * bar_length + "⬜" * (10 - bar_length)
            embed.add_field(
                name="✅ **Confirmations**",
                value=f"{conf_bar}\n**{tx['confirmations']}** confirmations",
                inline=False
            )
            
            # Network Fee
            embed.add_field(
                name="⛽ **Network Fee**",
                value=f"**{tx['network_fee']}** {tx['payment_method']}",
                inline=True
            )
            
            # Status
            status_emoji = "🟢" if tx['status'] == "Completed" else "🟡"
            embed.add_field(
                name="📊 **Status**",
                value=f"{status_emoji} **{tx['status']}**",
                inline=True
            )
            
            # Explorer link
            explorer_url = f"https://blockchair.com/{tx['payment_method'].lower()}/transaction/{tx['full_hash']}"
            embed.add_field(
                name="🔍 **View on Explorer**",
                value=f"[Click to view]({explorer_url})",
                inline=True
            )
            
            # Footer
            embed.set_footer(
                text=f"🟢 IGitems Middleman • 24/7 Secure • {tx['time']}",
                icon_url=self.avatar_url
            )
            
            # Send the transaction
            await channel.send(embed=embed)
            
            # Store transaction in history
            self.transaction_history.append(tx)
            if len(self.transaction_history) > 100:
                self.transaction_history.pop(0)
            
            print(f"✅ Posted transaction #{tx['order_number']} - {tx['payment_method']} ${tx['deal_amount']}")
            
        except Exception as e:
            print(f"❌ Error posting transaction: {e}")

    @post_transaction.before_loop
    async def before_post_transaction(self):
        """Wait for bot to be ready before starting"""
        await self.bot.wait_until_ready()
        print("📊 Transaction loop started")

    # ==================== COMMANDS ====================

    @commands.command(name='status')
    async def status(self, ctx):
        """Check bot status"""
        embed = discord.Embed(
            title="🤖 **IGitems Bot Status**",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=self.avatar_url)
        embed.set_image(url=self.banner_url)
        
        embed.add_field(
            name="📊 **Status**",
            value="🟢 **Online**" if self.post_transaction.is_running() else "🔴 Offline",
            inline=True
        )
        embed.add_field(
            name="💰 **Transactions**",
            value=f"**{len(self.transaction_history):,}**",
            inline=True
        )
        embed.add_field(
            name="⏰ **Interval**",
            value="**2** minutes",
            inline=True
        )
        
        if self.transaction_history:
            last = self.transaction_history[-1]
            embed.add_field(
                name="📋 **Last Transaction**",
                value=f"#{last['order_number']}\n${last['deal_amount']:,.2f}",
                inline=False
            )
        
        embed.set_footer(text="IGitems Premium Bot", icon_url=self.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='lasttx')
    async def last_transaction(self, ctx):
        """Show the last transaction"""
        if not self.transaction_history:
            await ctx.send("❌ No transactions have been posted yet!")
            return
        
        tx = self.transaction_history[-1]
        
        embed = discord.Embed(
            title=f"📋 **Last Transaction**",
            color=tx['color'],
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=self.avatar_url)
        
        embed.add_field(name="📋 Order", value=f"#{tx['order_number']:,}", inline=True)
        embed.add_field(name="💳 Payment", value=tx['payment_method'], inline=True)
        embed.add_field(name="💰 Amount", value=f"${tx['deal_amount']:,.2f}", inline=True)
        embed.add_field(name="⭐ Rating", value=f"{'⭐' * tx['rating']}", inline=True)
        embed.add_field(name="✅ Confirmations", value=str(tx['confirmations']), inline=True)
        embed.add_field(name="📊 Status", value=tx['status'], inline=True)
        embed.add_field(name="🔗 Hash", value=f"`{tx['transaction_hash']}`", inline=False)
        
        embed.set_footer(text=f"Posted at {tx['time']}", icon_url=self.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='forcetx')
    @commands.has_permissions(administrator=True)
    async def force_transaction(self, ctx):
        """Force post a transaction (admin only)"""
        try:
            tx = self.generate_transaction()
            
            embed = discord.Embed(
                title="🟢 **IGitems Transactions Bot**",
                description="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                color=tx['color'],
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=self.avatar_url)
            embed.set_image(url=self.banner_url)
            
            embed.add_field(name="\u200b", value=f"✅ **Transaction {tx['status']}**", inline=False)
            embed.add_field(name="\u200b", value=f"📋 **Order #{tx['order_number']:,}**", inline=False)
            embed.add_field(name="💳 Payment", value=f"{tx['emoji']} {tx['payment_method']}", inline=True)
            embed.add_field(name="💰 Amount", value=f"${tx['deal_amount']:,.2f}", inline=True)
            
            stars = "⭐" * tx['rating'] + "☆" * (5 - tx['rating'])
            embed.add_field(name="🏆 Rating", value=f"{stars}", inline=True)
            embed.add_field(name="👤 Trader", value=tx['trader'], inline=True)
            embed.add_field(name="🔖 Order ID", value=f"`{tx['order_id']}`", inline=True)
            embed.add_field(name="⛓️ Blockchain", value=tx['payment_method'], inline=True)
            embed.add_field(name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", inline=False)
            embed.add_field(name="🔗 Hash", value=f"```\n{tx['transaction_hash']}\n```", inline=False)
            embed.add_field(name="✅ Confirmations", value=str(tx['confirmations']), inline=True)
            embed.add_field(name="⛽ Fee", value=f"{tx['network_fee']}", inline=True)
            
            explorer_url = f"https://blockchair.com/{tx['payment_method'].lower()}/transaction/{tx['full_hash']}"
            embed.add_field(name="🔍 Explorer", value=f"[Click here]({explorer_url})", inline=True)
            
            embed.set_footer(text=f"🟢 IGitems Middleman • {tx['time']}", icon_url=self.avatar_url)
            
            await ctx.send("**⚡ Manual Transaction Posted**", embed=embed)
            self.transaction_history.append(tx)
            await ctx.send(f"✅ Transaction #{tx['order_number']} posted manually!")
            
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name='stats')
    async def stats(self, ctx):
        """Show detailed statistics"""
        if not self.transaction_history:
            await ctx.send("📊 No transactions available for statistics!")
            return
        
        total = len(self.transaction_history)
        total_amount = sum(tx['deal_amount'] for tx in self.transaction_history)
        avg_amount = total_amount / total if total > 0 else 0
        
        methods = [tx['payment_method'] for tx in self.transaction_history]
        most_used = max(set(methods), key=methods.count)
        
        completed = sum(1 for tx in self.transaction_history if tx['status'] == 'Completed')
        avg_rating = sum(tx['rating'] for tx in self.transaction_history) / total
        
        embed = discord.Embed(
            title="📊 **Transaction Statistics**",
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=self.avatar_url)
        embed.set_image(url=self.banner_url)
        
        embed.add_field(name="📋 **Total**", value=f"**{total:,}**", inline=True)
        embed.add_field(name="💰 **Volume**", value=f"**${total_amount:,.2f}**", inline=True)
        embed.add_field(name="📈 **Average**", value=f"**${avg_amount:,.2f}**", inline=True)
        embed.add_field(name="🏆 **Top Method**", value=f"**{most_used}**", inline=True)
        embed.add_field(name="✅ **Completed**", value=f"**{completed}/{total}**", inline=True)
        embed.add_field(name="⭐ **Rating**", value=f"**{avg_rating:.1f}/5**", inline=True)
        
        embed.set_footer(text="IGitems Analytics", icon_url=self.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show all available commands"""
        embed = discord.Embed(
            title="📚 **IGitems Bot Commands**",
            description="Here are all the available commands:",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=self.avatar_url)
        
        commands_list = [
            ("!status", "Check bot status and stats"),
            ("!lasttx", "Show the last posted transaction"),
            ("!stats", "View transaction statistics"),
            ("!forcetx", "Force post a transaction (Admin only)"),
            ("!help", "Show this help menu")
        ]
        
        for cmd, desc in commands_list:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        embed.set_footer(text="IGitems Premium Bot", icon_url=self.avatar_url)
        await ctx.send(embed=embed)

# ==================== BOT EVENTS ====================

@bot.event
async def on_ready():
    print("=" * 50)
    print("🚀 IGitems Transaction Bot is ONLINE!")
    print("=" * 50)
    print(f"👤 Logged in as: {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📊 Connected to {len(bot.guilds)} servers")
    print(f"📡 Posting transactions every 2 minutes")
    print("=" * 50)
    
    # Add the cog
    await bot.add_cog(TransactionBot(bot))
    print("✅ Cog loaded successfully")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"❌ Error in {event}: {args}")

# ==================== MAIN ====================

if __name__ == "__main__":
    print("=" * 50)
    print("⏳ Starting IGitems Transaction Bot...")
    print("=" * 50)
    
    if not TOKEN:
        print("❌ FATAL: DISCORD_TOKEN not found!")
        print("Please set DISCORD_TOKEN in your environment variables.")
        exit(1)
    
    if CHANNEL_ID == 0:
        print("⚠️ WARNING: CHANNEL_ID not set!")
        print("Please set CHANNEL_ID in your environment variables.")
        print("The bot will still run, but won't post transactions.")
    
    # Wait before connecting to avoid rate limits
    print("⏳ Waiting 5 seconds before connecting...")
    time.sleep(5)
    
    try:
        print("🔗 Attempting to connect to Discord...")
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ Invalid token! Please check your DISCORD_TOKEN.")
        exit(1)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        exit(1)
