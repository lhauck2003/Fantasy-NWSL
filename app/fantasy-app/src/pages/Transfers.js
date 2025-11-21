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

  if (!team) return (<p>Team loading...</p>)
    //setTeam(defaultTeam()); // set to default id no team: user needs to create one

  const formationRows = [
    { label: "Goalkeeper", key: "goalkeeper" },
    { label: "Defenders", key: "defenders" },
    { label: "Midfielders", key: "midfielders" },
    { label: "Forwards", key: "forwards" },
  ];

  // Helper to map position to group
  function getGroupKeyByPosition(position) {
    const pos = (position || "").toUpperCase();
    if (pos === "G") return "goalkeeper";
    if (pos === "D") return "defenders";
    if (pos === "M") return "midfielders";
    if (pos === "F") return "forwards";
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

  const isFirstList = first.groupKey === "transferIn";
  const isSecondList = second.groupKey === "transferIn";

  const isFirstTeam = !isFirstList;
  const isSecondTeam = !isSecondList;

  // -------------------------------------------------------
  // Only list ↔ team swaps allowed
  // -------------------------------------------------------
  if (isFirstTeam && isSecondTeam) {
    setSelectedPlayer(null);
    return;
  }
  if (isFirstList && isSecondList) {
    setSelectedPlayer(second);
    return;
  }

  const listPlayer = isFirstList ? first : second;
  const teamPlayer = isFirstTeam ? first : second;

  const targetGroup = teamPlayer.groupKey; // player must replace same position slot

  const incoming = listPlayer.player;
  const outgoing = teamPlayer.player;

  // -------------------------------------------------------
  // **CHECK #1: Position must match**
  // -------------------------------------------------------
  const incomingPos = incoming.position || incoming.pos || incoming.player_position;
  const outgoingPos = outgoing.position || outgoing.pos || outgoing.player_position;

  if (incomingPos !== outgoingPos) {
    alert(`Position mismatch: ${incomingPos} cannot replace ${outgoingPos}`);
    setSelectedPlayer(null);
    return;
  }

  // -------------------------------------------------------
  // Build new team object
  // -------------------------------------------------------
  const newTeam = {
    goalkeeper: [...team.goalkeeper],
    defenders: [...team.defenders],
    midfielders: [...team.midfielders],
    forwards: [...team.forwards],
    substitutes: [...team.substitutes],
  };

  // remove outgoing player from their slot
  newTeam[targetGroup] = newTeam[targetGroup].filter(
    p => p.player_id !== outgoing.player_id
  );

  // -------------------------------------------------------
  // **CHECK #2: Prevent duplicates**
  // -------------------------------------------------------
  const allPlayers = Object.values(newTeam).flat();
  const alreadyHasPlayer = allPlayers.some(
    p => p.player_id === incoming.player_id
  );

  if (alreadyHasPlayer) {
    alert("You already have this player on your team.");
    setSelectedPlayer(null);
    return;
  }

  // add incoming player to slot
  newTeam[targetGroup].push({ ...incoming });

  // -------------------------------------------------------
  // Formation rules (optional, keep your existing ones)
  // -------------------------------------------------------
  if (newTeam.goalkeeper.length !== 1) {
    alert("You must have exactly one goalkeeper.");
    setSelectedPlayer(null);
    return;
  }
  if (newTeam.defenders.length < 3) {
    alert("At least 3 defenders required.");
    setSelectedPlayer(null);
    return;
  }
  if (newTeam.forwards.length < 1) {
    alert("At least one forward required.");
    setSelectedPlayer(null);
    return;
  }

  // -------------------------------------------------------
  // Apply new team
  // -------------------------------------------------------
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
                  key={player.player_id}
                  className={`player-slot ${selectedPlayer?.player.player_id === player.player_id ? "selected" : ""}`}
                  onClick={() => handlePlayerClick(player, row.key)}
                >
                  <div className="slot-name">{player.player}</div>
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
              key={player.player_id}
              className={`bench-slot ${selectedPlayer?.player.player_id === player.player_id ? "selected" : ""}`}
              onClick={() => handlePlayerClick(player, "substitutes")}
            >
              <div className="slot-name">{player.player}</div>
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
            <option value="G">Goalkeepers</option>
            <option value="D">Defenders</option>
            <option value="M">Midfielders</option>
            <option value="F">Forwards</option>
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
              key={player.player_id}
              className={`player-list-item ${selectedPlayer?.player.player_id === player.player_id ? "selected" : ""}`}
              onClick={() => handlePlayerClick(player, "transferIn")}
            >
              <div className="list-name">{player.player}</div>
              <div className="list-pos">{player.position}</div>
              <div className="list-team">{player.team}</div>
              <div className="list-price">${player.price}M</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
