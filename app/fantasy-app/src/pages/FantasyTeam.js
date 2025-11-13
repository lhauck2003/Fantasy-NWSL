import { useState } from 'react';
import { NavigationBar, PageFooter, PageHeader } from './Main.js'


function TeamForm() {
    const [save, setSave] = useState(false);
    const [error, setError] = useState(null);
    const [status, setStatus] = useState('save');

    async function handleSave(e) {
      e.preventDefault();
      setStatus('saving');

      try {
        await saveTeamData(); // Assume saveTeamData is a function that saves the team data
        setSave(true);
        setStatus('Saved');

      }
      catch (err) {
        setStatus('error');
        setError(err)
      }

    }

    function handlePlayerChange(e) {
      // Handle player selection changes
    }

    function saveTeamData(e) {
      // save team data, send to backend
      e.preventDefault();

    }

    return (
      <>  
      <form id="team-form" onSubmit={handleSave} class = "team-form"> 
        <br />
        <button disabled={save===false || status==='save'}>{status}</button>

      </form>
      </>
    )
}

function TeamPage() {
  return (
    <div id="team-page">
      <NavigationBar />
      <TeamForm/>
    </div>
  )
}

export default TeamPage;