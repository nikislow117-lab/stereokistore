import discord
from discord.ext import commands, tasks
import logging
import random
from datetime import datetime
from config import Config
import aiohttp
import io

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

class PremiumIGitemsBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.order_counter = 480000
        self.transaction_history = []
        # Your image URLs
        self.avatar_url = "https://i.imgur.com/axv2qqm.png"
        self.banner_url = "https://i.imgur.com/CewEePA.png"
        self.post_transaction.start()

    def cog_unload(self):
        self.post_transaction.cancel()

    def generate_igitems_transaction(self):
        """Generate a realistic transaction"""
        self.order_counter += 1
        
        # Payment methods with emojis and colors
        payment_methods = {
            'Dogecoin': {'emoji': '🐕', 'color': 0xC2A633},
            'Bitcoin': {'emoji': '₿', 'color': 0xF7931A},
            'Ethereum': {'emoji': '⟠', 'color': 0x627EEA},
            'Litecoin': {'emoji': 'Ł', 'color': 0x345D9D},
            'Solana': {'emoji': '◎', 'color': 0x9945FF},
            'USDC': {'emoji': '💎', 'color': 0x2775CA},
            'Tether': {'emoji': '₮', 'color': 0x26A17B},
            'Cardano': {'emoji': '₳', 'color': 0x0033AD},
            'Monero': {'emoji': 'ɱ', 'color': 0xFF6600}
        }
        
        # Random selection
        payment_method = random.choice(list(payment_methods.keys()))
        method_data = payment_methods[payment_method]
        
        # Generate realistic amounts
        deal_amount = round(random.uniform(50, 500), 2)
        if random.random() < 0.2:  # 20% chance for big transaction
            deal_amount = round(random.uniform(500, 5000), 2)
        
        # Generate transaction hash
        tx_hash = ''.join(random.choices('0123456789abcdef', k=64))
        formatted_hash = f"{tx_hash[:20]}...{tx_hash[-20:]}"
        
        # Random confirmations
        confirmations = random.randint(10, 150)
        
        # Rating (mostly 5 stars)
        rating = random.choices([5, 4, 5, 5, 5], weights=[60, 10, 10, 10, 10])[0]
        
        # Order ID
        order_id = f"IG-{''.join(random.choices('0123456789ABCDEF', k=10))}"
        
        # Status
        status = random.choices(['Completed', 'Completed', 'Completed', 'Processing'])[0]
        
        # Current time
        current_time = datetime.now().strftime('%m/%d/%y, %I:%M %p')
        
        # Trader names
        traders = ['CryptoWhale', 'MoonTrader', 'DiamondHands', 'PandaTrades', 'FoxTrader']
        
        return {
            'order_number': self.order_counter,
            'payment_method': payment_method,
            'emoji': method_data['emoji'],
            'color': method_data['color'],
            'deal_amount': deal_amount,
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

    @tasks.loop(seconds=Config.POST_INTERVAL)
    async def post_transaction(self):
        """Post premium IGitems style transaction"""
        try:
            channel = self.bot.get_channel(Config.CHANNEL_ID)
            if not channel:
                logger.error(f"Channel {Config.CHANNEL_ID} not found!")
                return

            # Generate transaction
            tx = self.generate_igitems_transaction()
            
            # Create premium embed
            embed = discord.Embed(
                title="🟢 **IGitems Transactions Bot**",
                description="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                color=tx['color'],
                timestamp=datetime.now()
            )
            
            # Set avatar as thumbnail
            embed.set_thumbnail(url=self.avatar_url)
            
            # Set banner as image
            embed.set_image(url=self.banner_url)
            
            # Status
            embed.add_field(
                name="\u200b",
                value=f"✅ **Transaction {tx['status']}**",
                inline=False
            )
            
            # Order
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
            
            # Trader
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
            
            # Store transaction
            self.transaction_history.append(tx)
            if len(self.transaction_history) > 50:
                self.transaction_history.pop(0)
            
            logger.info(f"✅ Posted transaction #{tx['order_number']}")
            
        except Exception as e:
            logger.error(f"❌ Error posting transaction: {e}")

    @post_transaction.before_loop
    async def before_post_transaction(self):
        await self.bot.wait_until_ready()

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
            value=f"**{Config.POST_INTERVAL // 60}** min",
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
        """Show last transaction"""
        if not self.transaction_history:
            await ctx.send("❌ No transactions found!")
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
            tx = self.generate_igitems_transaction()
            
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
            
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name='stats')
    async def stats(self, ctx):
        """Show detailed statistics"""
        if not self.transaction_history:
            await ctx.send("No data available!")
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

# Setup
@bot.event
async def on_ready():
    logger.info(f"✅ Premium IGitems Bot is ready!")
    logger.info(f"👤 Logged in as {bot.user}")
    logger.info(f"📊 Posting transactions every {Config.POST_INTERVAL} seconds")
    logger.info(f"🖼️ Using avatar: {bot.user.display_avatar.url}")
    await bot.add_cog(PremiumIGitemsBot(bot))

if __name__ == "__main__":
    if not Config.DISCORD_TOKEN:
        logger.error("❌ DISCORD_TOKEN not found in .env file!")
        exit(1)
    
    if Config.CHANNEL_ID == 0:
        logger.error("❌ CHANNEL_ID not found in .env file!")
        exit(1)
    
    bot.run(Config.DISCORD_TOKEN)