import React, { useState, useEffect } from "react";
import "./Players.css";
import { api_network } from "../App";

export default function Players() {
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);

  const [selectedTeam, setSelectedTeam] = useState("");
  const [selectedPosition, setSelectedPosition] = useState("");
  const [priceCap, setPriceCap] = useState("");
  const [gamesMin, setGamesMin] = useState("");
  const [startsMin, setStartsMin] = useState("");

  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: null,
  });

  // -------------------------------------------
  // COLUMN DEFINITIONS — USED FOR HEADER + CELLS
  // -------------------------------------------
  const columns = [
    { key: "player", label: "Player" },
    { key: "position", label: "Position" },
    { key: "team", label: "Team" },
    { key: "price", label: "Price" },
    { key: "goals", label: "Goals" },
    { key: "assists", label: "Assists" },
    { key: "goals_assists", label: "Goal Contributions"},
    { key: "goals_per90", label: "Goals/90" },
    { key: "assists_per90", label: "Assists/90" },
    { key: "goals_assists_per90", label: "G+A/90" },
    { key: "minutes", label: "Minutes"}, // need to update data to store minutes as integer
    { key: "games", label: "Games"},
    { key: "games_starts", label: "Starts" },
    { key: "xg", label: "xG" },
    { key: "xg_assist", label: "xA" },
    { key: "xg_per90", label: "xG/90" },
    { key: "xg_assist_per90", label: "xA/90" },
    { key: "xg_xg_assist_per90", label: "xG+xA/90" },
  ];

  useEffect(() => {
    async function loadPlayers() {
      const p = await get_players();
      setPlayers(p);
      setFilteredPlayers(p);
    }
    loadPlayers();
  }, []);

  useEffect(() => {
    let result = [...players];

    if (selectedTeam) result = result.filter(p => p.team === selectedTeam);
    if (selectedPosition) result = result.filter(p => p.position === selectedPosition);
    if (priceCap) result = result.filter(p => p.price <= parseFloat(priceCap));
    if (gamesMin) result = result.filter(p => p.games >= parseInt(gamesMin));
    if (startsMin) result = result.filter(p => p.games_starts >= parseInt(startsMin));

    if (sortConfig.key && sortConfig.direction) {
      result.sort((a, b) => {
        const A = a[sortConfig.key];
        const B = b[sortConfig.key];

        if (A < B) return sortConfig.direction === "asc" ? -1 : 1;
        if (A > B) return sortConfig.direction === "asc" ? 1 : -1;
        return 0;
      });
    }

    setFilteredPlayers(result);
  }, [players, selectedTeam, selectedPosition, priceCap, sortConfig, gamesMin, startsMin]);

  const teamsList = Array.from(new Set(players.map(p => p.team))).sort();

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

  // Sorting cycle handler
  function sortBy(columnKey) {
    setSortConfig(prev => {
      if (prev.key !== columnKey) {
        return { key: columnKey, direction: "desc" };
      }
      if (prev.direction === "desc") {
        return { key: columnKey, direction: "asc" };
      }
      return { key: null, direction: null }; // reset
    });
  }

  function headerLabel(col) {
    if (sortConfig.key !== col.key) return col.label;
    if (sortConfig.direction === "desc") return col.label + " ↓";
    if (sortConfig.direction === "asc") return col.label + " ↑";
    return col.label;
  }

  function headerClass(col) {
    if (sortConfig.key !== col.key) return "";
    return sortConfig.direction === "asc" ? "sorted-asc" : "sorted-desc";
  }

  // Format cell contents depending on type
  function renderCell(player, col) {
    const value = player[col.key];

    // add link reference to player name
    if (col.key === "player") {
        let player_name = player.player.replaceAll(" ", "-")
        return (
            <span className="player-name">
                <a href={`https://fbref.com/en/players/${player.player_id}/${player_name}`} target="_blank" rel="noreferrer">{value}</a>
            </span>
                );
    }
    if (col.key === "price") return `$${value}M`;

    if (col.key === "position") {
      return <span className={`pos-chip ${value}`}>{value}</span>;
    }

    if (col.key === "team") {
      return <span className="team-tag">{value}</span>;
    }


    return value;
  }

  return (
    <div className="stats-table-container">
      <h1>Player Stats</h1>

      <div className="filter-bar">
        <select
          className="filter-select"
          value={selectedTeam}
          onChange={e => setSelectedTeam(e.target.value)}
        >
          <option value="">All Teams</option>
          {teamsList.map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>

        <select
          className="filter-select"
          value={selectedPosition}
          onChange={e => setSelectedPosition(e.target.value)}
        >
          <option value="">All Positions</option>
          <option value="G">Goalkeepers</option>
          <option value="D">Defenders</option>
          <option value="M">Midfielders</option>
          <option value="F">Forwards</option>
        </select>

        <select
          className="filter-select"
          value={priceCap}
          onChange={e => setPriceCap(e.target.value)}
        >
          <option value="">Price ≤ Any</option>
          <option value="4">≤ $4M</option>
          <option value="5">≤ $5M</option>
          <option value="6">≤ $6M</option>
          <option value="7">≤ $7M</option>
          <option value="8">≤ $8M</option>
        </select>
        <select
          className="filter-select"
          value={gamesMin}
          onChange={e => setGamesMin(e.target.value)}
        >
          <option value="">Any Games</option>
          <option value="5">5 ≤ Games</option>
          <option value="10">10 ≤ Games</option>
          <option value="15">15 ≤ Games</option>
          <option value="20">20 ≤ Games</option>
        </select>
        <select
          className="filter-select"
          value={startsMin}
          onChange={e => setStartsMin(e.target.value)}
        >
          <option value="">Any Starts</option>
          <option value="5">5 ≤ Starts</option>
          <option value="10">10 ≤ Starts</option>
          <option value="15">15 ≤ Starts</option>
          <option value="20">20 ≤ Starts</option>
        </select>
      </div>

      <div className="stats-table-wrapper">
        <table className="stats-table">
          <thead>
            <tr>
              {columns.map(col => (
                <th
                  key={col.key}
                  className={headerClass(col)}
                  onClick={() => sortBy(col.key)}
                >
                  {headerLabel(col)}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {filteredPlayers.map(player => (
              <tr key={player.player_id}>
                {columns.map(col => (
                  <td key={col.key} className={col.key === "goals" || col.key === "assists" || col.key === "price" ? "numeric" : ""}>
                    {renderCell(player, col)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
