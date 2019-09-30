import React from 'react';
import App from './App';
import axios from 'axios';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

jest.mock('axios')

const res = {
  data: {
    artists: [{"display_name": "Georges-Pierre Seurat", "token": "georgpierrseurat", "moma_url": "moma.org/artists/5358"}, {"display_name": "Paul C\u00e9zanne", "token": "paulc\u00e9zann", "moma_url": "moma.org/artists/1053"}, {"display_name": "Paul Gauguin", "token": "paulgauguin", "moma_url": "moma.org/artists/2098"}, {"display_name": "Vincent van Gogh", "token": "vincentvangogh", "moma_url": "moma.org/artists/2206"}],
    errors: null,
    title: "Cézanne, Gauguin, Seurat, Van Gogh",
    url: "moma.org/calendar/exhibitions/1767"
  }
}

describe('<App />', () => {
  it('renders a header element', () => {
    axios.get.mockResolvedValue(res)
    const wrapper = shallow(<App />)
    expect(wrapper.find('.App-header').length).toEqual(1)
  });

  it('sets the state using getData()', async () => {
    axios.get.mockResolvedValue(res)
    const wrapper = await shallow(<App />)
    expect(wrapper.state().exhibition.title).toEqual('Cézanne, Gauguin, Seurat, Van Gogh')
  });

  it('displays a title', async () => {
    axios.get.mockResolvedValue(res)
    const wrapper = await shallow(<App />)
    expect(wrapper.find('.App-header').text()).toContain('Cézanne, Gauguin, Seurat, Van Gogh')
  });

  it('renders a list of artists', async () => {
    axios.get.mockResolvedValue(res)
    const wrapper = await shallow(<App />);
    expect(wrapper.find('ul').children().length).toEqual(4)
  });
});
