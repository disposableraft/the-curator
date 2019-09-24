import React from 'react';
import App from './App';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('<App />', () => {
  it('has a header class', () => {
    const wrapper = shallow(<App />)
    expect(wrapper.find('.App-header').length).toEqual(1)
  });
});
