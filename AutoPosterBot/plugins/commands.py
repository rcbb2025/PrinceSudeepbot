import re
import base64
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
from AutoPosterBot.utils import decode, encode, temp, get_wish, get_size, LANGUAGE_MAP
from config import *

# Reusable Main Menu Buttons
def get_main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('🗃️ᴄʜᴀɴɴᴇʟ⚡', url=CHNL_LNK),
         InlineKeyboardButton('📢ɢʀᴏᴜᴘ🎭', url=GRP_LNK)],
        [InlineKeyboardButton('🥀ʜᴇʟᴘ✨', callback_data='help'),
         InlineKeyboardButton('👤ᴀʙᴏᴜᴛ⚙️', callback_data='about')]
    ])

# /start Command Handler
@Client.on_message(filters.command('start'))
async def start(client, message):
    mention = message.from_user.mention
    wish = get_wish()

    # If just /start
    if len(message.command) == 1:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(mention, wish),
            reply_markup=get_main_buttons(),
            parse_mode=enums.ParseMode.HTML
        )
        return

    # If /start <encoded-data>
    base64_string = message.command[1]
    try:
        decoded_string = await decode(base64_string)
        if '-' not in decoded_string:
            raise ValueError("Invalid format")

        command, converted_id = decoded_string.split('-')
        if command != 'get':
            raise ValueError("Invalid command")

        message_id = int(converted_id) // abs(LOG_CHANNEL)
        file = await client.get_messages(LOG_CHANNEL, message_id)

        if file.document:
            media = file.document
            send_func = message.reply_document
        elif file.video:
            media = file.video
            send_func = message.reply_video
        else:
            await message.reply_text("<b>The message does not contain a document or video.</b>")
            return

        caption = f"<b>{file.caption}</b>" if file.caption else "<b>Here is your file.</b>"
        sent_file = await send_func(media.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        notice = await sent_file.reply_text(
            "<b>❗️ This file will auto-delete in <u>10 minutes</u> due to copyright. Please save/forward it ⏰</b>",
            quote=True
        )

        await asyncio.sleep(600)
        await sent_file.delete()
        await notice.delete()

    except Exception as e:
        await message.reply_text(f"<b>⚠️ Error:</b> Invalid start parameter or internal error.")

# Callback Query Handler
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    mention = query.from_user.mention
    wish = get_wish()

    try:
        if data == "about":
            buttons = [
                [InlineKeyboardButton('📲 ᴀᴜᴛʜᴏʀ ⚡', user_id=885675538),
                 InlineKeyboardButton('🤖 sᴏᴜʀᴄᴇ 🤖', callback_data='source')],
                [InlineKeyboardButton('💰 ᴅᴏɴᴀᴛɪᴏɴ ᴍᴇ 💰', callback_data='donation')],
                [InlineKeyboardButton('🛰️ ʀᴇɴᴅᴇʀɪɴɢ sᴛᴀᴛᴜꜱ ☁️', callback_data='rendr')],
                [InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='start')]
            ]
            media = InputMediaPhoto(media=random.choice(PICS), caption=script.ABOUT_TXT.format(mention, wish), parse_mode=enums.ParseMode.HTML)
            await query.message.edit_media(media, reply_markup=InlineKeyboardMarkup(buttons))

        elif data == "source":
            buttons = [
                [InlineKeyboardButton('sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 📜', url='https://github.com.git'),
                 InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='about')]
            ]
            media = InputMediaPhoto(media=random.choice(PICS), caption=script.SOURCE_TXT, parse_mode=enums.ParseMode.HTML)
            await query.message.edit_media(media, reply_markup=InlineKeyboardMarkup(buttons))

        elif data == "donation":
            buttons = [
                [InlineKeyboardButton('💸 ᴄᴏᴘʏ ᴜᴘɪ 💸', url='https://t.me/share/url?url=smdowner@ybl'),
                 InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='about')]
            ]
            media = InputMediaPhoto(media=random.choice(PICS), caption=script.DONATION_TXT.format(mention, wish), parse_mode=enums.ParseMode.HTML)
            await query.message.edit_media(media, reply_markup=InlineKeyboardMarkup(buttons))

        elif data == "rendr":
            await query.answer(
                "⚡️ sᴛᴀᴛᴜs ⚡️\n\n"
                "❂ ʀᴀᴍ ●●●●●●●◌◌◌\n"
                "✇ ᴄᴘᴜ ●●●●●●●◌◌◌\n"
                "✪ ᴅᴀᴛᴀ ᴛʀᴀꜰɪᴄꜱ ●●●●◌◌◌◌◌◌ 🛰\n\n"
                "[sᴛᴀʙʟᴇ]",
                show_alert=True
            )

        elif data == "help":
            buttons = [[InlineKeyboardButton('⇋ ʙᴀᴄᴋ ⇋', callback_data='start')]]
            media = InputMediaPhoto(media=random.choice(PICS), caption=script.HELP_TXT.format(mention, wish), parse_mode=enums.ParseMode.HTML)
            await query.message.edit_media(media, reply_markup=InlineKeyboardMarkup(buttons))

        elif data == "start":
            media = InputMediaPhoto(media=random.choice(PICS), caption=script.START_TXT.format(mention, wish), parse_mode=enums.ParseMode.HTML)
            try:
                await query.message.edit_media(media, reply_markup=get_main_buttons())
            except Exception:
                await query.message.edit_text(script.START_TXT.format(mention, wish), reply_markup=get_main_buttons(), parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        await query.answer("⚠️ Something went wrong.", show_alert=True)


# Poster Creator and is Variables and is caption and more 
import re
import base64
import asyncio
import aiohttp
from Script import script
from pyrogram import Client, filters, enums
from AutoPosterBot.utils import decode, encode, temp, get_wish, get_size, LANGUAGE_MAP
from config import LOG_CHANNEL, POSTER_CHANNEL  # Add TMDB_API_KEY to your config
from AutoPosterBot.database.userdb import Database

# Initialize database
db = Database()

# TMDB Configuration
TMDB_API_KEY = "dbfeec55072d7f659ba0c76cd1cbda47"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # High quality poster size

def clean_title_for_search(title):
    """Clean title for better TMDB search results"""
    # Remove common prefixes and suffixes
    title = re.sub(r'^(@\w+\s*[-\s]*|TMV\s*[-\s]*|TBL\s*[-\s]*)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*\(.*?\)\s*', '', title)  # Remove anything in parentheses
    title = re.sub(r'\s*\[.*?\]\s*', '', title)  # Remove anything in brackets
    title = re.sub(r'[\.\-_]+', ' ', title)  # Replace dots, dashes, underscores with spaces
    title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with single space
    return title.strip()

async def get_movie_poster(title, year=None):
    """Search for movie and return poster info"""
    try:
        async with aiohttp.ClientSession() as session:
            # Clean title for better search results
            clean_title = clean_title_for_search(title)
            
            # Search URL
            search_url = f"{TMDB_BASE_URL}/search/movie"
            params = {
                'api_key': TMDB_API_KEY,
                'query': clean_title,
                'language': 'en-US',
                'page': 1
            }
            
            if year and year != "Unknown Year":
                params['year'] = year
            
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    if results:
                        # Get the first result (most relevant)
                        movie = results[0]
                        poster_path = movie.get('poster_path')
                        
                        if poster_path:
                            poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                            return {
                                'poster_url': poster_url,
                                'title': movie.get('title', title),
                                'release_date': movie.get('release_date', ''),
                                'overview': movie.get('overview', ''),
                                'vote_average': movie.get('vote_average', 0),
                                'tmdb_id': movie.get('id')
                            }
    except Exception as e:
        print(f"Error searching movie: {e}")
    return None

async def get_tv_series_poster(title, year=None):
    """Search for TV series and return poster info"""
    try:
        async with aiohttp.ClientSession() as session:
            # Clean title for better search results
            clean_title = clean_title_for_search(title)
            
            # Search URL
            search_url = f"{TMDB_BASE_URL}/search/tv"
            params = {
                'api_key': TMDB_API_KEY,
                'query': clean_title,
                'language': 'en-US',
                'page': 1
            }
            
            if year and year != "Unknown Year":
                params['first_air_date_year'] = year
            
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    if results:
                        # Get the first result (most relevant)
                        tv_show = results[0]
                        poster_path = tv_show.get('poster_path')
                        
                        if poster_path:
                            poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                            return {
                                'poster_url': poster_url,
                                'title': tv_show.get('name', title),
                                'first_air_date': tv_show.get('first_air_date', ''),
                                'overview': tv_show.get('overview', ''),
                                'vote_average': tv_show.get('vote_average', 0),
                                'tmdb_id': tv_show.get('id')
                            }
    except Exception as e:
        print(f"Error searching TV series: {e}")
    return None

def is_web_series_file(text):
    if not text:
        return False
    pattern = r'S\d{1,2}\s*[\.\- ]*(?:E|EP)\s*\d{1,2}'
    return bool(re.search(pattern, text, re.IGNORECASE))

def extract_season_episode(text):
    pattern = r'S(\d{1,2})\s*[\.\- ]*(?:E|EP)\s*(\d{1,2})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def extract_series_title(text):
    title = re.sub(r'S\d{1,2}\s*[\.\- ]*(?:E|EP)\s*\d{1,2}.*$', '', text, flags=re.IGNORECASE).strip()
    title = re.sub(r'[\[\(]\d{4}[\]\)]', '', title).strip()
    title = re.sub(r'^(@\w+\s*[-\s]*|TMV\s*[-\s]*|TBL\s*[-\s]*)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[\.\-]{2,}', ' ', title)
    return title.strip(' -.')

def extract_quality(text):
    if not text:
        return "Unknown Quality"
    quality_matches = re.findall(r'(?:\d{3,4}p)', text, re.IGNORECASE)
    # Remove duplicates
    seen = set()
    unique_qualities = [x.lower() for x in quality_matches if not (x.lower() in seen or seen.add(x.lower()))]
    unique_qualities.sort(key=lambda x: int(x[:-1]))
    return ', '.join(unique_qualities) if unique_qualities else "Unknown Quality"

def is_multi_language_file(caption):
    multi_lang_pattern = r'\[[^\]]*\+[^\]]*\]'
    return bool(re.search(multi_lang_pattern, caption, re.IGNORECASE))

def extract_languages_from_caption(caption):
    languages = set()
    # Only process if it's a multi-language file
    if not is_multi_language_file(caption):
        # For single language files, use existing LANGUAGE_MAP method
        file_languages = [
            full_name for abbr, full_name in LANGUAGE_MAP.items() 
            if re.search(rf'\b{abbr}\b', caption, re.IGNORECASE)
        ]
        return file_languages if file_languages else ["Unknown Language"]
    
    # Comprehensive language mapping for multi-language files
    language_mapping = {
        # English
        'eng': 'English', 'english': 'English', 'en': 'English',
        # Hindi
        'hin': 'Hindi', 'hindi': 'Hindi', 'hi': 'Hindi',
        # Tamil
        'tam': 'Tamil', 'tamil': 'Tamil', 'ta': 'Tamil',
        # Telugu
        'tel': 'Telugu', 'telugu': 'Telugu', 'te': 'Telugu',
        # Malayalam
        'mal': 'Malayalam', 'malayalam': 'Malayalam', 'ml': 'Malayalam',
        # Kannada
        'kan': 'Kannada', 'kannada': 'Kannada', 'kn': 'Kannada',
        # Bengali
        'ben': 'Bengali', 'bengali': 'Bengali', 'bn': 'Bengali', 'bangla': 'Bengali',
        # Gujarati
        'guj': 'Gujarati', 'gujarati': 'Gujarati', 'gu': 'Gujarati',
        # Marathi
        'mar': 'Marathi', 'marathi': 'Marathi', 'mr': 'Marathi',
        # Punjabi
        'pun': 'Punjabi', 'punjabi': 'Punjabi', 'pa': 'Punjabi',
        # Urdu
        'urd': 'Urdu', 'urdu': 'Urdu', 'ur': 'Urdu',
        # International Languages
        'spa': 'Spanish', 'spanish': 'Spanish', 'es': 'Spanish',
        'fre': 'French', 'french': 'French', 'fr': 'French', 'fra': 'French',
        'ger': 'German', 'german': 'German', 'de': 'German', 'deu': 'German',
        'ita': 'Italian', 'italian': 'Italian', 'it': 'Italian',
        'por': 'Portuguese', 'portuguese': 'Portuguese', 'pt': 'Portuguese',
        'rus': 'Russian', 'russian': 'Russian', 'ru': 'Russian',
        'chi': 'Chinese', 'chinese': 'Chinese', 'zh': 'Chinese', 'mandarin': 'Chinese',
        'jpn': 'Japanese', 'japanese': 'Japanese', 'ja': 'Japanese',
        'kor': 'Korean', 'korean': 'Korean', 'ko': 'Korean',
        'ara': 'Arabic', 'arabic': 'Arabic', 'ar': 'Arabic'
    }
    
    # Find languages in brackets with + symbol
    bracket_pattern = r'\[([^\]]*\+[^\]]*)\]'
    bracket_matches = re.findall(bracket_pattern, caption, re.IGNORECASE)
    
    for match in bracket_matches:
        # Split by + and clean up
        parts = re.split(r'\s*\+\s*', match)
        for part in parts:
            part = part.strip().lower()
            if part in language_mapping:
                languages.add(language_mapping[part])
    
    return sorted(list(languages)) if languages else ["Unknown Language"]

@Client.on_message(filters.channel & (filters.document | filters.video) & filters.chat(LOG_CHANNEL))  
async def post(client, message):  
    try:  
        if message.chat.id == LOG_CHANNEL and message.sender_chat and message.sender_chat.id == (await client.get_me()).id:  
            return  
        if message.chat.id != LOG_CHANNEL:  
            post_message = await message.copy(chat_id=LOG_CHANNEL, disable_notification=True)  
        else:  
            post_message = message  
          
        converted_id = post_message.id * abs(LOG_CHANNEL)  
        base64_string = await encode(f"get-{converted_id}")  
        bot_username = temp.U_NAME  
        link = f"https://t.me/{bot_username}?start={base64_string}"  
        
        # Media -- File Name And File Caption 
        media = message.document or message.video  
        file_name = media.file_name if media and media.file_name else "File"  
        file_caption = message.caption if message.caption else ""

        # Web Series 
        if is_web_series_file(file_name) or is_web_series_file(file_caption):
            print(f"Processing web series file: {file_caption}")
            
            # Series information
            season_num, episode_num = extract_season_episode(file_caption or file_name)
            series_title = extract_series_title(file_name)
            quality = extract_quality(file_caption)
            languages = extract_languages_from_caption(file_caption)
            
            # Extract year from caption
            year_match = re.search(r'(\d{4})', file_caption)
            year = year_match.group(1) if year_match else None
            
            # Get file size
            file_size = get_size(media.file_size)
            file_size_bytes = media.file_size
            print(f"Series: {series_title}, Season: {season_num}, Episode: {episode_num}, Quality: {quality}")
            
            # Create file info
            file_info = {
                'file_name': file_name,
                'caption': file_caption,
                'size': file_size,
                'size_bytes': file_size_bytes,
                'link': link,
                'quality': quality,
                'languages': languages,
                'season': season_num,
                'episode': episode_num
            }
            
            # Create series key (group by series and season)
            series_key = f"WEBSERIES_{series_title}_S{season_num:02d}"
            
            # Check if series already exists
            existing_series = db.get_movie(series_key)
            
            if existing_series:
                print(f"Series exists, adding episode {episode_num}")
                
                # Check for duplicate
                duplicate_found = False
                for existing_file in existing_series.get('files', []):
                    if (existing_file.get('episode') == episode_num and 
                        existing_file.get('quality') == quality):
                        print(f"Duplicate found: S{season_num:02d}E{episode_num:02d} {quality}")
                        duplicate_found = True
                        break
                
                if duplicate_found:
                    return
                
                # Add new file
                db.add_file_to_movie(series_key, file_info)
                updated_series = db.get_movie(series_key)
                
                # Process all files and group by episode
                episodes = {}
                all_languages = set()
                all_qualities = set()
                
                for file_data in updated_series['files']:
                    ep_num = file_data.get('episode', 1)
                    file_quality = file_data.get('quality', 'Unknown Quality')
                    
                    if ep_num not in episodes:
                        episodes[ep_num] = {}
                    
                    episodes[ep_num][file_quality] = file_data['link']
                    
                    # Collect all languages and qualities
                    if file_data.get('languages'):
                        all_languages.update(file_data['languages'])
                    
                    if file_quality != 'Unknown Quality':
                        all_qualities.add(file_quality)
                
                # Build episode list
                episode_lines = []
                for ep_num in sorted(episodes.keys()):
                    quality_links = []
                    for qual in sorted(episodes[ep_num].keys()):
                        quality_links.append(f"<a href='{episodes[ep_num][qual]}'>{qual}</a>")
                    
                    episode_lines.append(f"<b>📦 EP{ep_num:02d} : {' | '.join(quality_links)}</b>")
                
                # Create updated caption
                language_text = ', '.join(sorted(all_languages)) if all_languages else "Unknown Language"
                quality_text = ', '.join(sorted(all_qualities)) if all_qualities else "Unknown Quality"
                
                updated_caption = f"<b>🎬 Title : {series_title}</b>\n"
                updated_caption += f"<b>📂 Season: {season_num}</b>\n"
                updated_caption += f"<b>🔊 Audio : {language_text}</b>\n"
                updated_caption += f"<b>💿 Quality : {quality_text}</b>\n\n"
                updated_caption += "\n".join(episode_lines)
                
                # Update existing message
                try:
                    await client.edit_message_text(
                        chat_id=POSTER_CHANNEL,
                        message_id=existing_series['message_id'],
                        text=updated_caption
                    )
                    print(f"Updated web series post: {series_title} S{season_num:02d}")
                except Exception as e:
                    print(f"Error updating web series post: {e}")
            
            else:
                print(f"Creating new series post: {series_title}")
                
                # Get TMDB poster for TV series
                poster_info = await get_tv_series_poster(series_title, year)
                
                # Create new series post
                language_text = ', '.join(languages)
                
                caption = f"<b>🎬 Title : {series_title}</b>\n"
                caption += f"<b>📂 Season: {season_num}</b>\n"
                caption += f"<b>🔊 Audio : {language_text}</b>\n"
                caption += f"<b>💿 Quality : {quality}</b>\n\n"
                caption += f"<b>📦 EP{episode_num:02d} : <a href='{link}'>{quality}</a></b>"
                
                # Send new message with or without photo
                if poster_info and poster_info.get('poster_url'):
                    try:
                        sent_message = await client.send_photo(
                            chat_id=POSTER_CHANNEL,
                            photo=poster_info['poster_url'],
                            caption=caption
                        )
                        print(f"Sent web series with poster: {series_title}")
                    except Exception as photo_error:
                        print(f"Error sending photo, sending text only: {photo_error}")
                        sent_message = await client.send_message(
                            chat_id=POSTER_CHANNEL,
                            text=caption
                        )
                else:
                    sent_message = await client.send_message(
                        chat_id=POSTER_CHANNEL,
                        text=caption
                    )
                sticker = "CAACAgQAAxkBAAEHzpFoZ9arY1ygtR-Wodb2d-aotwsplAACnjgAAjGNRgABOsdMK2pVZ7keBA"
                await client.send_sticker(
                    chat_id=POSTER_CHANNEL,
                    sticker=sticker
                )
                
                # Save to database
                series_data = {
                    'title': series_title,
                    'season': season_num,
                    'year': year,
                    'message_id': sent_message.id,
                    'files': [file_info],
                    'type': 'webseries',
                    'poster_info': poster_info
                }
                
                await db.save_movie(series_key, series_data)
                print(f"Created new web series post: {series_title} S{season_num:02d}")
        
        else:
            # Movie Processing 
            print(f"Processing movie file: {file_name}")
            
            file_caption = message.caption.split('\n')[0] if message.caption else ""
            
            # Movie Title
            title_text = file_caption if file_caption else file_name
            movie_title = re.sub(r'^(@\w+\s*[-\s]*|TMV\s*[-\s]*|TBL\s*[-\s]*)', '', title_text, flags=re.IGNORECASE)
            movie_title = re.split(r'\s*\(?\d{4}\)?|\s+(?:BR-?Rip|WEB-?Rip|HD|720p|1080p|x264|x265)', movie_title)[0]
            movie_title = movie_title.strip(' -.')
            
            # Movie Year
            year_match = re.search(r'(\d{4})', file_caption)
            year = year_match.group(1) if year_match else "Unknown Year"
            
            # Movie Quality
            quality_matches = re.findall(r'(?:\d{3,4}p|HQ|HDRip|4K|PreDVD|WEB-DL|BDRip|DVDScr|CAM|TS|SCR|VODRip|Remux|R5|SDTV|TVRip|HDTV|UNRATED|EXTENDED)', file_caption, re.IGNORECASE)
            current_quality = ', '.join(quality_matches) if quality_matches else "Unknown Quality"
            
            # Extract languages using improved method
            file_languages = extract_languages_from_caption(file_caption)
            
            # File Size
            if message.document:
                file_size = get_size(message.document.file_size)
                file_size_bytes = message.document.file_size
            elif message.video:  
                file_size = get_size(message.video.file_size)
                file_size_bytes = message.video.file_size
            else:  
                file_size = "N/A"
                file_size_bytes = 0
            
            # Create file info
            file_info = {
                'caption': file_caption,
                'size': file_size,
                'size_bytes': file_size_bytes,
                'link': link,
                'quality': current_quality,
                'languages': file_languages
            }
            
            # Create movie key based on whether it's multi-language or not
            if is_multi_language_file(file_caption):
                # For multi-language files, use only title and year (group together)
                movie_key = f"{movie_title}_{year}"
            else:
                # For single language files, include language in key (separate posts)
                language_text = ', '.join(file_languages)
                movie_key = f"{movie_title}_{year}_{language_text}"
                
            existing_movie = db.get_movie(movie_key)
            
            if existing_movie:
                if db.check_file_exists(movie_key, file_caption):
                    print(f"Duplicate file detected, skipping: {file_caption}")
                    return
                    
                # Movie exists, add new file and update post
                db.add_file_to_movie(movie_key, file_info)
                updated_movie = db.get_movie(movie_key)
            
                # Collect all unique languages from all files
                all_languages = set()
                all_qualities = set()
            
                for file_data in updated_movie['files']:
                    if 'languages' in file_data:
                        all_languages.update(file_data['languages'])
                        
                    file_qualities = file_data['quality'].split(', ')
                    all_qualities.update([q.strip() for q in file_qualities if q.strip() != "Unknown Quality"])
                    
                # Create combined language and quality text
                language_text = ', '.join(sorted(all_languages)) if all_languages else "Unknown Language"
                quality_text = ', '.join(sorted(all_qualities)) if all_qualities else "Unknown Quality"
            
                # Sort files by size (smallest to largest)
                sorted_files = sorted(updated_movie['files'], key=lambda x: x['size_bytes'])
            
                # Build file list
                file_list = []
                for file_data in sorted_files:
                    file_list.append(f"<b>{file_data['caption']}</b>\n<b>({file_data['size']}) : <a href='{file_data['link']}'>Get File</a></b>")
                    
                # Create updated caption
                updated_caption = (
                    f"<b>🎬 Title : {movie_title}</b>\n"
                    f"<b>📆 Year : {year}</b>\n"
                    f"<b>🔊 Audio : {language_text}</b>\n"
                    f"<b>💿 Quality : {quality_text}</b>\n\n"
                    + "\n\n".join(file_list)
                )
                
                # Edit existing message
                try:
                    # Check if original message has photo
                    if updated_movie.get('poster_info'):
                        await client.edit_message_caption(
                            chat_id=POSTER_CHANNEL,
                            message_id=existing_movie['message_id'],
                            caption=updated_caption
                        )
                    else:
                        await client.edit_message_text(
                            chat_id=POSTER_CHANNEL,
                            message_id=existing_movie['message_id'],
                            text=updated_caption
                        )
                    print(f"Updated existing post for: {movie_title}")
                    file_sizes = [file_data['size'] for file_data in sorted_files]
                    print(f"Files in size order: {' → '.join(file_sizes)}")
                    print(f"Combined languages: {language_text}")
                except Exception as edit_error:
                    print(f"Error editing message: {edit_error}")
            else:
                # New movie, create new post
                language_text = ', '.join(file_languages)
                caption = (
                    f"<b>🎬 Title : {movie_title}</b>\n"
                    f"<b>📆 Year : {year}</b>\n"
                    f"<b>🔊 Audio : {language_text}</b>\n"
                    f"<b>💿 Quality : {current_quality}</b>\n\n"
                    f"<b>{file_caption}</b>\n"
                    f"<b>({file_size}) : <a href='{link}'>Get File</a></b>"
                )
                
                # Get TMDB poster for movie
                poster_info = await get_movie_poster(movie_title, year if year != "Unknown Year" else None)
                
                # Send new message with or without photo
                if poster_info and poster_info.get('poster_url'):
                    try:
                        sent_message = await client.send_photo(
                            chat_id=POSTER_CHANNEL,
                            photo=poster_info['poster_url'],
                            caption=caption
                        )
                        print(f"Sent movie with poster: {movie_title}")
                    except Exception as photo_error:
                        print(f"Error sending photo, sending text only: {photo_error}")
                        sent_message = await client.send_message(
                            chat_id=POSTER_CHANNEL,
                            text=caption
                        )
                else:
                    sent_message = await client.send_message(
                        chat_id=POSTER_CHANNEL,
                        text=caption
                    )
                sticker = "CAACAgQAAxkBAAEHzpFoZ9arY1ygtR-Wodb2d-aotwsplAACnjgAAjGNRgABOsdMK2pVZ7keBA"
                await client.send_sticker(
                    chat_id=POSTER_CHANNEL,
                    sticker=sticker
                )
                
                # Save to database
                movie_data = {
                    'title': movie_title,
                    'year': year,
                    'message_id': sent_message.id,
                    'files': [file_info],
                    'poster_info': poster_info
                }
                await db.save_movie(movie_key, movie_data)
                print(f"Created new post for: {movie_title}")
    except Exception as e:
        print(f"Error in post function: {e}")

