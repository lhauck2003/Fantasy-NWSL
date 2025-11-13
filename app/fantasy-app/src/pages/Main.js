function NavigationBar() {
  return (
    <div id="main-page">
      <PageHeader/>
      <header>Fantasy NWSL</header>
      <ul id="main_nav">
          <li><a aria-current="page" class = "main_nav" href="/">Home</a></li> 
          <li><a class = "main_nav" href="/players">Players</a></li>
          <li><a class = "main_nav" href="/leagues">Leagues</a></li>
          <li><a class = "main_nav" href="/team">My Team</a></li>
          <li><a class = "main_nav" href="/transfers">Transfers</a></li>
          <li><a class = "main_nav" href="/points">Week Points</a></li>
          <li><a class = "main_nav" href="/login">Login</a></li> 
      </ul>
      </div>
  );
}

function PageHeader() {
  return (
      <head>
        <meta charset="UTF-8"></meta>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
        <title>Fantasy NWSL</title>
        <meta name="author" content="Levi Hauck"></meta>
        <link rel="stylesheet" type="text/css" href="/Fantasy-NWSL/app/static/css/style.css"></link>
      </head>
  );
}

function PageFooter() {
  return (
    <footer>
    <p> Fantasy NWSL&trade;</p>
    </footer>
  )
}

export {NavigationBar, PageFooter, PageHeader};