import React, {Fragment} from 'react'

const url = 'http://localhost:8000/api/bookmarks';


class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            todos: [],
        }
    }

    async fetchTodos() {
        try {
            const response = await fetch(url, {mode: 'cors'});
            const data = await response.json();
            this.setState({
                todos: data['bookmarks'].map(bookmark => {
                    bookmark.url = `http://localhost:8000${bookmark.url}`;
                    return bookmark;
                })
            });
        } catch (error) {
            console.log(error);
        }
    }

    async componentDidMount() {
        console.log('App component mounted')
        await this.fetchTodos();
        this.setState({loading: false})
    }

    render() {
        if (this.state.todos.length === 0 || this.state.loading) {
            return <Fragment>Loading...</Fragment>
        } else {
            return (
                <Fragment>
                    <h1>Bookmarks</h1>
                    <ul>
                        {this.state.todos.map((todo) => (
                            <li key={todo.id}>
                                <a title={todo.title} href={todo.url} target='_blank' rel="noreferrer">{todo.title}</a>
                            </li>
                        ))}
                    </ul>
                </Fragment>
            )
        }
    }
}

export default App