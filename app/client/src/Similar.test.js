import React from 'react';
import Similar from './Similar';
import axios from 'axios';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

jest.mock('axios')
jest.mock('vis')

const route = { params: { token: 'louisnevelson' } }

const res = {
  data: { "original_token": "louisnevelson", "artists": [{ "display_name": "Allan D'Arcangelo", "token": "allanarcangelo", "moma_url": "moma.org/artists/1349" }, { "display_name": "Helen Frankenthaler", "token": "helenfrankenthal", "moma_url": "moma.org/artists/1974" }, { "display_name": "Carl Andre", "token": "carlandr", "moma_url": "moma.org/artists/174" }, { "display_name": "Milton Avery", "token": "miltonaveri", "moma_url": "moma.org/artists/250" }, { "display_name": "Robert Rauschenberg", "token": "robertrauschenberg", "moma_url": "moma.org/artists/4823" }, { "display_name": "Claes Oldenburg", "token": "claeoldenburg", "moma_url": "moma.org/artists/4397" }, { "display_name": "Alex Katz", "token": "alexkatz", "moma_url": "moma.org/artists/3016" }, { "display_name": "Sigmar Polke", "token": "sigmarpolk", "moma_url": "moma.org/artists/4671" }, { "display_name": "Joan Mitchell", "token": "joanmitchel", "moma_url": "moma.org/artists/4026" }, { "display_name": "Roy Lichtenstein", "token": "roilichtenstein", "moma_url": "moma.org/artists/3542" }] }
}

describe('<Similar />', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue(res)
  });

  it('renders a header element', () => {
    const wrapper = shallow(<Similar match={route} />)
    expect(wrapper.find('.Similar-header').length).toEqual(1)
  });
});