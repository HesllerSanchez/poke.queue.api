import json 
import logging

from fastapi import HTTPException
from models.PokeRequest import PokemonRequest
from utils.database import execute_query_json
from utils.AQueue import AQueue

# configurar el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def select_pokemon_request( id: int ):
    try:
        query = "select * from pokequeue.requests where id = ?"
        params = (id,)
        result = await execute_query_json( query , params )
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        logger.error( f"Error selecting report request {e}" )
        raise HTTPException( status_code=500 , detail="Internal Server Error" )


async def update_pokemon_request( pokemon_request: PokemonRequest) -> dict:
    try:
        query = " exec pokequeue.update_poke_request ?, ?, ? "
        if not pokemon_request.url:
            pokemon_request.url = "";

        params = ( pokemon_request.id, pokemon_request.status, pokemon_request.url  )
        result = await execute_query_json( query , params, True )
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        logger.error( f"Error updating report request {e}" )
        raise HTTPException( status_code=500 , detail="Internal Server Error" )


async def insert_pokemon_request( pokemon_request: PokemonRequest) -> dict:
    try:
        query = " exec pokequeue.create_poke_request ? "
        params = ( pokemon_request.pokemon_type,  )
        result = await execute_query_json( query , params, True )
        result_dict = json.loads(result)

        await AQueue().insert_message_on_queue( result )

        return result_dict
    except Exception as e:
        logger.error( f"Error inserting report reques {e}" )
        raise HTTPException( status_code=500 , detail="Internal Server Error" )