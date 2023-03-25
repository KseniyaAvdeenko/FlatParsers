import logo_flat from "./img/logo_flat.png"
import React from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Flats from "./components/Flats";
import Flat from "./components/Flat";

function BaseLayout(){
    return (
        <div className="wrapper">
           <header className="header header_size header_bg-color">
                <div className="flex-container">
                    <div className="logo">
                        <img src={logo_flat} alt="" className="logo__img" width="58" height="54"/>
                    </div>
                </div>
            </header>
            <Routes>
                <Route path="/" element={<Flats/>}/>
                <Route path="/:flat_id" element={<Flat/>}/>
            </Routes>
            <footer className="footer footer_size header_bg-color ">
                <div className="flex-container">
                    <div className="copyrights">Made by K. Avdeenko</div>
                </div>
            </footer>
        </div>
    )
}

function App() {
  return (
    <BrowserRouter>
        <BaseLayout/>
    </BrowserRouter>
  );
}

export default App;
