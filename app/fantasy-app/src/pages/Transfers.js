import React, { useEffect, useState } from "react";
import "./Transfers.css";
import { api_network, local_api_network } from "../App";

export default function Transfers({ userID }) {
  const [team, setTeam] = useState(null);
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [selectedPosition, setSelectedPosition] = useState("");
  const [priceSort, setPriceSort] = useState("");

  // Load team
  useEffect(() => {
    async function loadTeam() {
      const t = await get_team(userID);
      setTeam(t);
    }
    loadTeam();
  }, [userID]);

  // Load players
  useEffect(() => {
    async function loadPlayers() {
      const p = await get_players();
      setPlayers(p);
      setFilteredPlayers(p);
    }
    loadPlayers();
  }, []);

  // Apply filters whenever filter state changes
  useEffect(() => {
    let filtered = [...players];

    if (selectedTeam) {
      filtered = filtered.filter(p => p.team === selectedTeam);
    }

    if (selectedPosition) {
      filtered = filtered.filter(p => p.position === selectedPosition);
    }

    if (priceSort === "asc") {
      filtered.sort((a, b) => a.price - b.price);
    } else if (priceSort === "desc") {
      filtered.sort((a, b) => b.price - a.price);
    }

    setFilteredPlayers(filtered);
  }, [players, selectedTeam, selectedPosition, priceSort]);

  // Fetch team from backend
  async function get_team(userID) {
    try {
      const response = await fetch(api_network + "/fetch_team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userID }),
      });
      if (response.ok) {
        return await response.json();
      }
    } catch (err) {
      console.error(err);
      alert("Team load failed");
    }
  }

  // Fetch players from backend
  async function get_players() {
    try {
      const response = await fetch(api_network + "/players", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ which: {} }),
      });
      if (response.ok) {
        const data = await response.json();
        return data.players;
      }
    } catch (err) {
      console.error(err);
      alert("Failed to load players");
    }
    return [];
  }

  if (!team) return <p>Loading team...</p>;

  const formationRows = [
    { label: "Goalkeeper", key: "goalkeeper" },
    { label: "Defenders", key: "defenders" },
    { label: "Midfielders", key: "midfielders" },
    { label: "Forwards", key: "forwards" },
  ];

  // Helper to map position to group
  function getGroupKeyByPosition(position) {
    const pos = (position || "").toUpperCase();
    if (pos === "GK") return "goalkeeper";
    if (pos === "DEF" || pos === "DF") return "defenders";
    if (pos === "MID" || pos === "MF") return "midfielders";
    if (pos === "FW" || pos === "FWD" || pos === "ST") return "forwards";
    return "midfielders";
  }

  // Handle player click (transfer in/out)
  function handlePlayerClick(player, groupKey) {
    if (!selectedPlayer) {
      setSelectedPlayer({ player, groupKey });
      return;
    }

    const first = selectedPlayer;
    const second = { player, groupKey };

    const isBenchFirst = first.groupKey === "substitutes";
    const isBenchSecond = second.groupKey === "substitutes";

    // Only allow bench/field <-> list swaps
    if (isBenchFirst === isBenchSecond) {
      setSelectedPlayer(null);
      return;
    }

    const bench = isBenchFirst ? first : second;
    const field = isBenchFirst ? second : first;

    const newTeam = {
      goalkeeper: [...team.goalkeeper],
      defenders: [...team.defenders],
      midfielders: [...team.midfielders],
      forwards: [...team.forwards],
      substitutes: [...team.substitutes],
    };

    newTeam.substitutes = newTeam.substitutes.filter(p => p.id !== bench.player.id);
    newTeam[field.groupKey] = newTeam[field.groupKey].filter(p => p.id !== field.player.id);

    newTeam.substitutes.push(field.player);
    const benchTargetGroup = getGroupKeyByPosition(bench.player.position);
    newTeam[benchTargetGroup].push(bench.player);

    // Validation
    if (newTeam.defenders.length < 3 || newTeam.goalkeeper.length !== 1 || newTeam.forwards.length < 1) {
      alert("Invalid team formation!");
      setSelectedPlayer(null);
      return;
    }

    setTeam(newTeam);
    setSelectedPlayer(null);
  }

  async function saveTeam() {
    try {
      const resp = await fetch("http://127.0.0.1:8000/save_team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userID, team }),
      });
      if (!resp.ok) throw new Error("Save failed");
      alert("Team saved");
    } catch (err) {
      console.error(err);
      alert("Save failed");
    }
  }

  const teamsList = Array.from(
    new Set(
      [
        ...players
      ].map(p => p.team)
    )
  ).sort();

  return (
    <div className="container">
      {/* Left: Fantasy Team */}
      <div className="fantasy-team-container">
        <h1>Make Transfers</h1>

        {/* Pitch */}
        <div className="pitch">
          {formationRows.map(row => (
            <div className="pitch-line" key={row.key}>
              {team[row.key].map(player => (
                <button
                  key={player.id}
                  className={`player-slot ${selectedPlayer?.player.id === player.id ? "selected" : ""}`}
                  onClick={() => handlePlayerClick(player, row.key)}
                >
                  <div className="slot-name">{player.name}</div>
                  <div className="slot-pos">{player.position}</div>
                </button>
              ))}
            </div>
          ))}
        </div>

        {/* Bench */}
        <h2>Bench</h2>
        <div className="bench-row">
          {team.substitutes.map(player => (
            <button
              key={player.id}
              className={`bench-slot ${selectedPlayer?.player.id === player.id ? "selected" : ""}`}
              onClick={() => handlePlayerClick(player, "substitutes")}
            >
              <div className="slot-name">{player.name}</div>
              <div className="slot-pos">{player.position}</div>
            </button>
          ))}
        </div>

        <button className="save-button" onClick={saveTeam}>Save Team</button>
      </div>

      {/* Right: Player List with Filters */}
      <div className="player-list-container">
        <h1>Players</h1>
        <div className="filter-bar">
          <select className="filter-select" value={selectedTeam} onChange={e => setSelectedTeam(e.target.value)}>
            <option value="">All Teams</option>
            {teamsList.map(team => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>

          <select className="filter-select" value={selectedPosition} onChange={e => setSelectedPosition(e.target.value)}>
            <option value="">All Positions</option>
            <option value="GK">Goalkeepers</option>
            <option value="DEF">Defenders</option>
            <option value="MID">Midfielders</option>
            <option value="FW">Forwards</option>
          </select>

          <select className="filter-select" value={priceSort} onChange={e => setPriceSort(e.target.value)}>
            <option value="">Sort by Price</option>
            <option value="asc">Low → High</option>
            <option value="desc">High → Low</option>
          </select>
        </div>

        <div className="player-list">
          {filteredPlayers.map(player => (
            <button
              key={player.id}
              className={`player-list-item ${selectedPlayer?.player.id === player.id ? "selected" : ""}`}
              onClick={() => handlePlayerClick(player, "transferIn")}
            >
              <div className="list-name">{player.name}</div>
              <div className="list-pos">{player.position}</div>
              <div className="list-team">{player.team}</div>
              <div className="list-price">${player.price}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
