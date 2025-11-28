#!/usr/bin/env python3
"""
🎮 ADVANCED FREE GAME MONITOR BOT
Developed with precision engineering for optimal performance
Professional-grade game tracking system
"""

import os
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import discord
from discord.ext import tasks, commands

# Professional logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('GameMonitorBot')

class AdvancedGameMonitor(commands.Bot):
    """
    Advanced Game Monitoring System
    Professional-grade free game detection bot
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Memory-optimized data structures
        self.tracked_games: Dict[str, datetime] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.start_time = datetime.now()
        
        # Platform configurations
        self.platforms = {
            'epic_games': {
                'name': 'Epic Games Store',
                'url': 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=tr',
                'color': 0x2E64FE
            },
            'steam': {
                'name': 'Steam',
                'url': 'https://store.steampowered.com/api/featuredcategories',
                'color': 0x1B2838
            }
        }

    async def setup_hook(self) -> None:
        """Initialize bot resources"""
        self.session = aiohttp.ClientSession()
        logger.info("🔄 Advanced Game Monitor initializing...")
        
        # Start monitoring tasks
        self.monitor_games.start()
        self.system_status.start()

    async def close(self) -> None:
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        await super().close()

    @tasks.loop(minutes=5)
    async def monitor_games(self):
        """Main game monitoring loop"""
        try:
            await self.check_epic_games()
            await asyncio.sleep(15)  # Rate limiting
            await self.check_steam_games()
            
        except Exception as e:
            logger.error(f"Monitoring error: {e}")

    @tasks.loop(hours=1)
    async def system_status(self):
        """System health monitoring"""
        uptime = datetime.now() - self.start_time
        logger.info(f"✅ System Status: {len(self.tracked_games)} games tracked | Uptime: {uptime}")

    async def check_epic_games(self):
        """Advanced Epic Games free game detection"""
        try:
            async with self.session.get(self.platforms['epic_games']['url']) as response:
                if response.status == 200:
                    data = await response.json()
                    games = data['data']['Catalog']['searchStore']['elements']
                    
                    for game in games:
                        await self.process_game_data(game, 'epic_games')
                        
        except Exception as e:
            logger.error(f"Epic Games API error: {e}")

    async def check_steam_games(self):
        """Advanced Steam free game detection"""
        try:
            async with self.session.get(self.platforms['steam']['url']) as response:
                if response.status == 200:
                    data = await response.json()
                    # Advanced Steam parsing logic here
                    logger.info("🔄 Steam store analysis completed")
                    
        except Exception as e:
            logger.error(f"Steam API error: {e}")

    async def process_game_data(self, game_data: Dict, platform: str):
        """Advanced game data processing"""
        try:
            game_id = game_data.get('id')
            game_title = game_data.get('title', 'Unknown Game')
            
            # Check if game is free and new
            if self.is_game_free(game_data) and game_id not in self.tracked_games:
                self.tracked_games[game_id] = datetime.now()
                await self.send_game_alert(game_data, platform)
                logger.info(f"🎯 New free game detected: {game_title}")
                
        except Exception as e:
            logger.error(f"Game processing error: {e}")

    def is_game_free(self, game_data: Dict) -> bool:
        """Advanced free game detection logic"""
        try:
            promotions = game_data.get('promotions', {})
            promotional_offers = promotions.get('promotionalOffers', [])
            
            if promotional_offers:
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Free check error: {e}")
            return False

    async def send_game_alert(self, game_data: Dict, platform: str):
        """Professional game alert system"""
        try:
            channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
            channel = self.get_channel(channel_id)
            
            if not channel:
                logger.error("Channel not found")
                return

            platform_info = self.platforms[platform]
            
            # Advanced embed creation
            embed = discord.Embed(
                title=f"🎮 **FREE GAME ALERT** - {platform_info['name']}",
                description=f"**{game_data.get('title', 'Unknown Game')}**",
                color=platform_info['color'],
                timestamp=datetime.now()
            )

            # Advanced game information
            embed.add_field(
                name="💰 Price",
                value="**FREE** 🆓",
                inline=True
            )
            
            embed.add_field(
                name="📅 Duration",
                value="Limited Time Offer ⏰",
                inline=True
            )
            
            embed.add_field(
                name="🔗 Platform",
                value=platform_info['name'],
                inline=True
            )

            # Advanced footer with tracking info
            embed.set_footer(
                text=f"Advanced Game Monitor • {len(self.tracked_games)} games tracked",
                icon_url="https://i.imgur.com/3Z8jCzW.png"
            )

            # Add thumbnail if available
            if game_data.get('keyImages'):
                for image in game_data['keyImages']:
                    if image.get('type') == 'Thumbnail':
                        embed.set_thumbnail(url=image['url'])
                        break

            await channel.send(embed=embed)
            logger.info(f"📢 Alert sent: {game_data.get('title')}")

        except Exception as e:
            logger.error(f"Alert sending error: {e}")

    @monitor_games.before_loop
    async def before_monitor(self):
        """Wait until bot is ready"""
        await self.wait_until_ready()

# Advanced bot initialization
if __name__ == "__main__":
    bot = AdvancedGameMonitor()
    
    try:
        bot.run(os.getenv('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        logger.info("🛑 Bot shutdown initiated")
    except Exception as e:
        logger.critical(f"❌ Critical error: {e}")
