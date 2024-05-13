class HTMLBuilder:

    def __init__(self):
        self.startingHTML = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                body {
                    background-color: #181818;;
                }
                .card{
                    background-color: #292929;
                    width: 700px;
                    padding: 20px 20px 20px 20px;
                    border-radius: 20px;
                    color: white;
                }
                p{color: rgb(185, 185, 185);}
                span{color: white;}
                ::-webkit-scrollbar {
                width: 20px;
                }
        
                ::-webkit-scrollbar-track {
                background-color: transparent;
                }
        
                ::-webkit-scrollbar-thumb {
                background-color: #00ACC1;
                border-radius: 20px;
                border: 6px solid transparent;
                background-clip: content-box;
                }
        
                ::-webkit-scrollbar-thumb:hover {
                background-color: rgb(0, 163, 181);
                }
            </style>
        </head>
        <body>
            <div style="margin: auto;width: 75%;">
        """
        self.endingHTML = """
            </div>
        </body>
        </html>
        """
        self.loadingHTML = "" + self.startingHTML
        self.loadingHTML += f"""
        <div class="card" style="text-align:center">
            <h1>Loading..</h1>
        </div><br>\n
        """
        self.loadingHTML += self.endingHTML

        self.TestHTML = "" + self.startingHTML
        self.TestHTML += f"""
                <div class="card" style="text-align:center">
                    <h1>A7a..</h1>
                </div><br>\n
                """
        self.TestHTML += self.endingHTML

    def buildHTML(self, data, isUniversity=False):
        fullHTML = "" + self.startingHTML
        if data:
            if isUniversity:
                for index, entry in enumerate(data):
                    result = entry.asdict()
                    fullHTML += f"""
                    <div class="card">
                        <h1>Result {index}</h1>
                    """
                    for variable, value in result.items():
                        fullHTML += f"""
                            <p>{variable}:  <span>{value}</span></p>
                        """
                    fullHTML += f"""
                    </div><br>\n
                    """
            else:
                for entry in data:
                    fullHTML += f"""
                    <div class="card">
                        <h1>{entry['title']['value']}</h1>
                        <p>{entry['abstract']['value']}</p><br>
                        <p>Country:      <span>{entry['countries']['value'] if 'countries' in entry and entry['countries']['value'] else 'Unknown'}</span></p>
                        <p>Genre:        <span>{entry['genres']['value'] if 'genres' in entry and entry['genres']['value'] else 'Unknown'}</span></p>
                        <p>Year:     <span>{entry['year']['value'] if 'year' in entry and entry['year']['value'] else 'Unknown'}</span></p>
                        <p>Director:     <span>{entry['directors']['value'] if 'directors' in entry and entry['directors']['value'] else 'Unknown'}</span></p>
                        <p>Cast:     <span>{entry['actors']['value'] if 'actors' in entry and entry['actors']['value'] else 'Unknown'}</span></p>
                    </div><br>\n
                    """
        else:
            fullHTML += f"""
            <div class="card" style="text-align:center">
                <h1>No Results Found</h1>
            </div><br>\n
            """
        fullHTML += self.endingHTML

        return fullHTML
