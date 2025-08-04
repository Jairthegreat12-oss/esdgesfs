/*
================================================================================
||                                                                            ||
||                           GAME CLIENT (C# - Unity Style)                     ||
||                                                                            ||
================================================================================

This C# code simulates how a game client (like one made in Unity or Godot)
would handle both the license key validation and the mod loading.

--------------------------------------------------------------------------------
-- File: GameManager.cs
--------------------------------------------------------------------------------
*/

using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
// This would typically be a JSON library like Newtonsoft.Json or Unity's JsonUtility
// For this example, we'll simulate it with a simple dictionary.
using SimpleJson; 

public class GameManager
{
    // --- License System Variables ---
    private static readonly HttpClient httpClient = new HttpClient();
    private const string API_URL = "http://127.0.0.1:5000/validate_key"; // Our local Python server
    private const string LICENSE_FILE = "license.dat";
    public bool IsLicensed { get; private set; } = false;

    // --- Modding System Variables ---
    public Dictionary<string, Item> gameItems = new Dictionary<string, Item>();
    private string modsPath = "Mods";

    // --- Game Entry Point ---
    public async Task Start()
    __p_
        Console.WriteLine("--- Starting Game ---");
        await CheckLicense();

        if (IsLicensed)
        {
            Console.WriteLine("License is valid. Welcome!");
            InitializeGameData();
            LoadMods();
            DisplayGameItems();
        }
        else
        {
            Console.WriteLine("This game requires a valid license key to play.");
            // In a real game, you would show a UI prompt to enter a key.
            // We'll simulate entering a key from the console.
            Console.Write("Enter license key: ");
            string key = Console.ReadLine();
            await ValidateKey(key);
            if(IsLicensed) {
                 // Relaunch or continue
                 Console.WriteLine("Key accepted! Please restart the game.");
            } else {
                 Console.WriteLine("Invalid key. Exiting.");
            }
        }
    }

    // --- License System Methods ---
    private async Task CheckLicense()
    {
        if (File.Exists(LICENSE_FILE))
        {
            string key = File.ReadAllText(LICENSE_FILE);
            await ValidateKey(key);
        }
    }

    private async Task ValidateKey(string key)
    {
        try
        {
            var response = await httpClient.GetStringAsync($"{API_URL}?key={key}");
            // In a real scenario, you'd parse a JSON response.
            if (response.Contains("\"status\": \"valid\""))
            {
                IsLicensed = true;
                File.WriteAllText(LICENSE_FILE, key); // Save the valid key
            }
            else
            {
                IsLicensed = false;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error validating key: {ex.Message}");
            IsLicensed = false;
        }
    }

    // --- Modding System Methods ---
    private void InitializeGameData()
    {
        Console.WriteLine("\n--- Loading Base Game Data ---");
        // In a real game, this would be loaded from a base 'data.json' file
        gameItems.Add("stone_pickaxe", new Item { Name = "Stone Pickaxe", Power = 5 });
        gameItems.Add("iron_shovel", new Item { Name = "Iron Shovel", Power = 3 });
    }

    private void LoadMods()
    {
        Console.WriteLine("\n--- Loading Mods ---");
        if (!Directory.Exists(modsPath))
        {
            Console.WriteLine("Mods folder not found. No mods will be loaded.");
            Directory.CreateDirectory(modsPath);
            return;
        }

        foreach (var directory in Directory.GetDirectories(modsPath))
        {
            string modName = new DirectoryInfo(directory).Name;
            string itemsFile = Path.Combine(directory, "items.json");
            if (File.Exists(itemsFile))
            {
                Console.WriteLine($"Found mod: {modName}");
                string json = File.ReadAllText(itemsFile);
                
                // Using a simulated JSON parser
                var modItems = SimpleJson.DeserializeObject<Dictionary<string, Item>>(json);

                foreach(var modItem in modItems)
                {
                    if(gameItems.ContainsKey(modItem.Key))
                    {
                        Console.WriteLine($"  - Overwriting item: {modItem.Key}");
                        gameItems[modItem.Key] = modItem.Value;
                    }
                    else
                    {
                        Console.WriteLine($"  - Adding new item: {modItem.Key}");
                        gameItems.Add(modItem.Key, modItem.Value);
                    }
                }
            }
        }
    }
    
    private void DisplayGameItems()
    {
        Console.WriteLine("\n--- Final Game Items ---");
        foreach(var item in gameItems)
        {
            Console.WriteLine($" - ID: {item.Key}, Name: {item.Value.Name}, Power: {item.Value.Power}");
        }
    }
}

// Helper classes to simulate game data and JSON parsing
public class Item
{
    public string Name { get; set; }
    public int Power { get; set; }
}

// Dummy JSON parser for demonstration purposes
namespace SimpleJson
{
    public static class SimpleJson
    {
        public static T DeserializeObject<T>(string json)
        {
            // This is a placeholder for a real JSON library like Newtonsoft.Json
            // It's not a real parser.
            var dict = new Dictionary<string, Item>();
            if(json.Contains("diamond_pickaxe")) {
                 dict.Add("diamond_pickaxe", new Item { Name = "Diamond Pickaxe", Power = 20 });
            }
            if(json.Contains("stone_pickaxe")) {
                 dict.Add("stone_pickaxe", new Item { Name = "Stone Pickaxe", Power = 7 });
            }
            return (T)Convert.ChangeType(dict, typeof(T));
        }
    }
}

// --- Program Entry ---
public class Program
{
    public static async Task Main(string[] args)
    {
        var gameManager = new GameManager();
        await gameManager.Start();
    }
}


/*
================================================================================
||                                                                            ||
||                      LICENSE SERVER (PYTHON - FLASK)                         ||
||                                                                            ||
================================================================================

This Python script runs a simple web server that acts as our license key
validator. You would run this on a server, and the C# game would communicate
with it over the internet.

--------------------------------------------------------------------------------
-- File: license_server.py
--------------------------------------------------------------------------------
*/

from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)
DB_FILE = "licenses.db"

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # A simple table: key is the unique license, is_used is a flag
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS license_keys (
            key TEXT PRIMARY KEY,
            is_used INTEGER DEFAULT 0,
            customer_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- API Endpoints ---

# This is for YOU, the developer, to generate keys. Not for the public.
@app.route('/generate_key', methods=['POST'])
def generate_key():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    new_key = str(uuid.uuid4()) # Generate a random UUID as the key
    cursor.execute("INSERT INTO license_keys (key) VALUES (?)", (new_key,))
    conn.commit()
    conn.close()
    print(f"Generated new key: {new_key}")
    return jsonify({"status": "success", "key": new_key})

# This is the public endpoint your GAME will call.
@app.route('/validate_key', methods=['GET'])
def validate_key():
    key_to_check = request.args.get('key')
    if not key_to_check:
        return jsonify({"status": "error", "message": "No key provided"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM license_keys WHERE key=?", (key_to_check,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"}), 404

if __name__ == '__main__':
    init_db()
    # To generate your first key, you can run a separate script or use a tool
    # like Postman to send a POST request to /generate_key
    print("License server is running. Use /generate_key (POST) to create keys.")
    print("Use /validate_key?key=... (GET) to check them.")
    app.run(port=5000, debug=True)

/*
================================================================================
||                                                                            ||
||                               MOD EXAMPLE                                  ||
||                                                                            ||
================================================================================

This shows the file structure and content for a sample mod.

--------------------------------------------------------------------------------
-- File Structure:
--------------------------------------------------------------------------------

/YourGameReleaseFolder/
|-- YourGame.exe
|-- license.dat (created automatically after successful validation)
|
|-- /Mods/
    |-- /SuperPickaxesMod/
        |-- items.json   <-- The mod file

--------------------------------------------------------------------------------
-- File: items.json (inside SuperPickaxesMod folder)
--------------------------------------------------------------------------------

{
    "stone_pickaxe": {
        "Name": "Stone Pickaxe",
        "Power": 7 
    },
    "diamond_pickaxe": {
        "Name": "Diamond Pickaxe",
        "Power": 20
    }
}

*/
