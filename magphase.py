<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  
  


  

  <head>
    <title>
      /trunk/gdal/swig/python/samples/magphase.py – GDAL
    </title>
        <link rel="search" href="/gdal/search" />
        <link rel="help" href="/gdal/wiki/TracGuide" />
        <link rel="alternate" href="/gdal/browser/trunk/gdal/swig/python/samples/magphase.py?format=txt" type="text/plain" title="Plain Text" /><link rel="alternate" href="/gdal/export/25415/trunk/gdal/swig/python/samples/magphase.py" type="text/x-python; charset=iso-8859-15" title="Original Format" />
        <link rel="up" href="/gdal/browser/trunk/gdal/swig/python/samples" title="Parent directory" />
        <link rel="start" href="/gdal/wiki" />
        <link rel="stylesheet" href="/gdal/chrome/common/css/trac.css" type="text/css" /><link rel="stylesheet" href="/gdal/chrome/common/css/code.css" type="text/css" /><link rel="stylesheet" href="/gdal/pygments/trac.css" type="text/css" /><link rel="stylesheet" href="/gdal/chrome/common/css/browser.css" type="text/css" />
        <link rel="shortcut icon" href="/gdal/chrome/common/trac.ico" type="image/x-icon" />
        <link rel="icon" href="/gdal/chrome/common/trac.ico" type="image/x-icon" />
      <link type="application/opensearchdescription+xml" rel="search" href="/gdal/search/opensearch" title="Search GDAL" />
    <script type="text/javascript" src="/gdal/chrome/common/js/jquery.js"></script><script type="text/javascript" src="/gdal/chrome/common/js/trac.js"></script><script type="text/javascript" src="/gdal/chrome/common/js/search.js"></script><script type="text/javascript" src="/gdal/chrome/tracsectionedit/js/tracsectionedit.js"></script>
    <!--[if lt IE 7]>
    <script type="text/javascript" src="/gdal/chrome/common/js/ie_pre7_hacks.js"></script>
    <![endif]-->
    <script type="text/javascript">
      jQuery(document).ready(function($) {
        $(".trac-toggledeleted").show().click(function() {
                  $(this).siblings().find(".trac-deleted").toggle();
                  return false;
        }).click();
        $("#jumploc input").hide();
        $("#jumploc select").change(function () {
          this.parentNode.parentNode.submit();
        });
      });
    </script>
  </head>
  <body>
    <div id="banner">
      <div id="header">
        <a id="logo" href="http://www.gdal.org/"><img src="/gdal/chrome/site/trac_logo.png" alt="GDAL" height="80" width="80" /></a>
      </div>
      <form id="search" action="/gdal/search" method="get">
        <div>
          <label for="proj-search">Search:</label>
          <input type="text" id="proj-search" name="q" size="18" value="" />
          <input type="submit" value="Search" />
        </div>
      </form>
      <div id="metanav" class="nav">
    <ul>
      <li class="first"><a href="/gdal/login">Login</a></li><li><a href="/gdal/wiki/TracGuide">Help/Guide</a></li><li><a href="/gdal/about">About Trac</a></li><li class="last"><a href="/gdal/prefs">Preferences</a></li>
    </ul>
  </div>
    </div>
    <div id="mainnav" class="nav">
    <ul>
      <li class="first"><a href="/gdal/wiki">Wiki</a></li><li><a href="/gdal/timeline">Timeline</a></li><li><a href="/gdal/roadmap">Roadmap</a></li><li class="active"><a href="/gdal/browser">Browse Source</a></li><li><a href="/gdal/report">View Tickets</a></li><li class="last"><a href="/gdal/search">Search</a></li>
    </ul>
  </div>
    <div id="main">
      <div id="ctxtnav" class="nav">
        <h2>Context Navigation</h2>
          <ul>
              <li class="first"><a href="/gdal/changeset/22986/trunk/gdal/swig/python/samples/magphase.py">Last Change</a></li><li><a href="/gdal/browser/trunk/gdal/swig/python/samples/magphase.py?annotate=blame&amp;rev=22986" title="Annotate each line with the last changed revision (this can be time consuming...)">Annotate</a></li><li class="last"><a href="/gdal/log/trunk/gdal/swig/python/samples/magphase.py">Revision Log</a></li>
          </ul>
        <hr />
      </div>
    <div id="content" class="browser">
      <h1>
    <a class="pathentry first" title="Go to root directory" href="/gdal/browser">root</a><span class="pathentry sep">/</span><a class="pathentry" title="View trunk" href="/gdal/browser/trunk">trunk</a><span class="pathentry sep">/</span><a class="pathentry" title="View gdal" href="/gdal/browser/trunk/gdal">gdal</a><span class="pathentry sep">/</span><a class="pathentry" title="View swig" href="/gdal/browser/trunk/gdal/swig">swig</a><span class="pathentry sep">/</span><a class="pathentry" title="View python" href="/gdal/browser/trunk/gdal/swig/python">python</a><span class="pathentry sep">/</span><a class="pathentry" title="View samples" href="/gdal/browser/trunk/gdal/swig/python/samples">samples</a><span class="pathentry sep">/</span><a class="pathentry" title="View magphase.py" href="/gdal/browser/trunk/gdal/swig/python/samples/magphase.py">magphase.py</a>
    <br style="clear: both" />
  </h1>
      <div id="jumprev">
        <form action="" method="get">
          <div>
            <label for="rev">
              View revision:</label>
            <input type="text" id="rev" name="rev" size="6" />
          </div>
        </form>
      </div>
      <div id="jumploc">
        <form action="" method="get">
          <div class="buttons">
            <label for="preselected">Visit:</label>
            <select id="preselected" name="preselected">
              <option selected="selected"></option>
              <optgroup label="branches">
                <option value="/gdal/browser/trunk">trunk</option><option value="/gdal/browser/branches/1.4">branches/1.4</option><option value="/gdal/browser/branches/1.5">branches/1.5</option><option value="/gdal/browser/branches/1.6">branches/1.6</option><option value="/gdal/browser/branches/1.7">branches/1.7</option><option value="/gdal/browser/branches/1.8">branches/1.8</option><option value="/gdal/browser/branches/1.9">branches/1.9</option>
              </optgroup><optgroup label="tags">
                <option value="/gdal/browser/tags/1.4.1?rev=11234">tags/1.4.1</option><option value="/gdal/browser/tags/1.4.2?rev=11712">tags/1.4.2</option><option value="/gdal/browser/tags/1.4.3?rev=12595">tags/1.4.3</option><option value="/gdal/browser/tags/1.4.4?rev=12953">tags/1.4.4</option><option value="/gdal/browser/tags/1.4.5?rev=15952">tags/1.4.5</option><option value="/gdal/browser/tags/1.5.0?rev=13414">tags/1.5.0</option><option value="/gdal/browser/tags/1.5.1?rev=14070">tags/1.5.1</option><option value="/gdal/browser/tags/1.5.2?rev=14575">tags/1.5.2</option><option value="/gdal/browser/tags/1.5.3?rev=15511">tags/1.5.3</option><option value="/gdal/browser/tags/1.5.4?rev=16068">tags/1.5.4</option><option value="/gdal/browser/tags/1.6.0?rev=15876">tags/1.6.0</option><option value="/gdal/browser/tags/1.6.1?rev=17005">tags/1.6.1</option><option value="/gdal/browser/tags/1.6.2?rev=17488">tags/1.6.2</option><option value="/gdal/browser/tags/1.6.3?rev=18095">tags/1.6.3</option><option value="/gdal/browser/tags/1.7.0?rev=18598">tags/1.7.0</option><option value="/gdal/browser/tags/1.7.1?rev=18764">tags/1.7.1</option><option value="/gdal/browser/tags/1.7.2?rev=19512">tags/1.7.2</option><option value="/gdal/browser/tags/1.7.3?rev=21099">tags/1.7.3</option><option value="/gdal/browser/tags/1.8.0?rev=21497">tags/1.8.0</option><option value="/gdal/browser/tags/1.8.1?rev=22733">tags/1.8.1</option><option value="/gdal/browser/tags/1.9.0?rev=23700">tags/1.9.0</option><option value="/gdal/browser/tags/1.9.1?rev=24999">tags/1.9.1</option><option value="/gdal/browser/tags/1.9.2?rev=25090">tags/1.9.2</option><option value="/gdal/browser/tags/gdal_1_1_5?rev=2477">tags/gdal_1_1_5</option><option value="/gdal/browser/tags/gdal_1_1_6?rev=2907">tags/gdal_1_1_6</option><option value="/gdal/browser/tags/gdal_1_1_7?rev=3128">tags/gdal_1_1_7</option><option value="/gdal/browser/tags/gdal_1_1_8?rev=4018">tags/gdal_1_1_8</option><option value="/gdal/browser/tags/gdal_1_1_9?rev=5024">tags/gdal_1_1_9</option><option value="/gdal/browser/tags/gdal_1_2_0?rev=5939">tags/gdal_1_2_0</option><option value="/gdal/browser/tags/gdal_1_2_1?rev=6269">tags/gdal_1_2_1</option><option value="/gdal/browser/tags/gdal_1_2_2?rev=6554">tags/gdal_1_2_2</option><option value="/gdal/browser/tags/gdal_1_2_3?rev=6599">tags/gdal_1_2_3</option><option value="/gdal/browser/tags/gdal_1_2_4?rev=6758">tags/gdal_1_2_4</option><option value="/gdal/browser/tags/gdal_1_2_5?rev=6820">tags/gdal_1_2_5</option><option value="/gdal/browser/tags/gdal_1_2_6?rev=7349">tags/gdal_1_2_6</option><option value="/gdal/browser/tags/gdal_1_3_0?rev=8081">tags/gdal_1_3_0</option><option value="/gdal/browser/tags/gdal_1_3_1?rev=8554">tags/gdal_1_3_1</option><option value="/gdal/browser/tags/gdal_1_3_2?rev=9679">tags/gdal_1_3_2</option><option value="/gdal/browser/tags/gdal_1_4_0?rev=10550">tags/gdal_1_4_0</option>
              </optgroup>
            </select>
            <input type="submit" value="Go!" title="Jump to the chosen preselected path" />
          </div>
        </form>
      </div>
      <table id="info" summary="Revision info">
        <tr>
          <th scope="col">
            Revision <a href="/gdal/changeset/22986">22986</a>, <span title="2052 bytes">2.0 KB</span>
            (checked in by rouault, <a class="timeline" href="/gdal/timeline?from=2011-08-27T07%3A20%3A16-0700&amp;precision=second" title="2011-08-27T07:20:16-0700 in Timeline">16 months</a> ago)
          </th>
        </tr>
        <tr>
          <td class="message searchable">
              <p>
set svn:executable bit<br />
</p>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <ul class="props">
              <li>
                  Property <strong>svn:executable</strong> set to
                    <em><code>*</code></em>
              </li>
            </ul>
          </td>
        </tr>
      </table>
      <div id="preview" class="searchable">
    <table class="code"><thead><tr><th class="lineno" title="Line numbers">Line</th><th class="content"> </th></tr></thead><tbody><tr><th id="L1"><a href="#L1">1</a></th><td><span class="c">#!/usr/bin/env python</span></td></tr><tr><th id="L2"><a href="#L2">2</a></th><td><span class="c">#******************************************************************************</span></td></tr><tr><th id="L3"><a href="#L3">3</a></th><td><span class="c"># </span></td></tr><tr><th id="L4"><a href="#L4">4</a></th><td><span class="c">#  Project:  GDAL</span></td></tr><tr><th id="L5"><a href="#L5">5</a></th><td><span class="c">#  Purpose:  Example computing the magnitude and phase from a complex image.</span></td></tr><tr><th id="L6"><a href="#L6">6</a></th><td><span class="c">#  Author:   Frank Warmerdam, warmerdam@pobox.com</span></td></tr><tr><th id="L7"><a href="#L7">7</a></th><td><span class="c"># </span></td></tr><tr><th id="L8"><a href="#L8">8</a></th><td><span class="c">#******************************************************************************</span></td></tr><tr><th id="L9"><a href="#L9">9</a></th><td><span class="c">#  Copyright (c) 2008, Frank Warmerdam &lt;warmerdam@pobox.com&gt;</span></td></tr><tr><th id="L10"><a href="#L10">10</a></th><td><span class="c"># </span></td></tr><tr><th id="L11"><a href="#L11">11</a></th><td><span class="c">#  Permission is hereby granted, free of charge, to any person obtaining a</span></td></tr><tr><th id="L12"><a href="#L12">12</a></th><td><span class="c">#  copy of this software and associated documentation files (the "Software"),</span></td></tr><tr><th id="L13"><a href="#L13">13</a></th><td><span class="c">#  to deal in the Software without restriction, including without limitation</span></td></tr><tr><th id="L14"><a href="#L14">14</a></th><td><span class="c">#  the rights to use, copy, modify, merge, publish, distribute, sublicense,</span></td></tr><tr><th id="L15"><a href="#L15">15</a></th><td><span class="c">#  and/or sell copies of the Software, and to permit persons to whom the</span></td></tr><tr><th id="L16"><a href="#L16">16</a></th><td><span class="c">#  Software is furnished to do so, subject to the following conditions:</span></td></tr><tr><th id="L17"><a href="#L17">17</a></th><td><span class="c"># </span></td></tr><tr><th id="L18"><a href="#L18">18</a></th><td><span class="c">#  The above copyright notice and this permission notice shall be included</span></td></tr><tr><th id="L19"><a href="#L19">19</a></th><td><span class="c">#  in all copies or substantial portions of the Software.</span></td></tr><tr><th id="L20"><a href="#L20">20</a></th><td><span class="c"># </span></td></tr><tr><th id="L21"><a href="#L21">21</a></th><td><span class="c">#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS</span></td></tr><tr><th id="L22"><a href="#L22">22</a></th><td><span class="c">#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,</span></td></tr><tr><th id="L23"><a href="#L23">23</a></th><td><span class="c">#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL</span></td></tr><tr><th id="L24"><a href="#L24">24</a></th><td><span class="c">#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER</span></td></tr><tr><th id="L25"><a href="#L25">25</a></th><td><span class="c">#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING</span></td></tr><tr><th id="L26"><a href="#L26">26</a></th><td><span class="c">#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER</span></td></tr><tr><th id="L27"><a href="#L27">27</a></th><td><span class="c">#  DEALINGS IN THE SOFTWARE.</span></td></tr><tr><th id="L28"><a href="#L28">28</a></th><td><span class="c">#******************************************************************************</span></td></tr><tr><th id="L29"><a href="#L29">29</a></th><td></td></tr><tr><th id="L30"><a href="#L30">30</a></th><td><span class="k">import</span> <span class="nn">gdal</span></td></tr><tr><th id="L31"><a href="#L31">31</a></th><td><span class="k">import</span> <span class="nn">gdalnumeric</span></td></tr><tr><th id="L32"><a href="#L32">32</a></th><td><span class="k">try</span><span class="p">:</span></td></tr><tr><th id="L33"><a href="#L33">33</a></th><td>    <span class="k">import</span> <span class="nn">numpy</span></td></tr><tr><th id="L34"><a href="#L34">34</a></th><td><span class="k">except</span><span class="p">:</span></td></tr><tr><th id="L35"><a href="#L35">35</a></th><td>    <span class="k">import</span> <span class="nn">Numeric</span> <span class="k">as</span> <span class="nn">numpy</span></td></tr><tr><th id="L36"><a href="#L36">36</a></th><td></td></tr><tr><th id="L37"><a href="#L37">37</a></th><td></td></tr><tr><th id="L38"><a href="#L38">38</a></th><td>src_ds <span class="o">=</span> gdal<span class="o">.</span>Open<span class="p">(</span><span class="s">'complex.tif'</span><span class="p">)</span></td></tr><tr><th id="L39"><a href="#L39">39</a></th><td>xsize <span class="o">=</span> src_ds<span class="o">.</span>RasterXSize</td></tr><tr><th id="L40"><a href="#L40">40</a></th><td>ysize <span class="o">=</span> src_ds<span class="o">.</span>RasterYSize</td></tr><tr><th id="L41"><a href="#L41">41</a></th><td></td></tr><tr><th id="L42"><a href="#L42">42</a></th><td>src_image <span class="o">=</span> src_ds<span class="o">.</span>GetRasterBand<span class="p">(</span><span class="mf">1</span><span class="p">)</span><span class="o">.</span>ReadAsArray<span class="p">()</span></td></tr><tr><th id="L43"><a href="#L43">43</a></th><td>mag_image <span class="o">=</span> <span class="nb">pow</span><span class="p">(</span>numpy<span class="o">.</span>real<span class="p">(</span>src_image<span class="p">)</span><span class="o">*</span>numpy<span class="o">.</span>real<span class="p">(</span>src_image<span class="p">)</span> \</td></tr><tr><th id="L44"><a href="#L44">44</a></th><td>                <span class="o">+</span> numpy<span class="o">.</span>imag<span class="p">(</span>src_image<span class="p">)</span><span class="o">*</span>numpy<span class="o">.</span>imag<span class="p">(</span>src_image<span class="p">),</span><span class="mf">0.5</span><span class="p">)</span></td></tr><tr><th id="L45"><a href="#L45">45</a></th><td>gdalnumeric<span class="o">.</span>SaveArray<span class="p">(</span> mag_image<span class="p">,</span> <span class="s">'magnitude.tif'</span> <span class="p">)</span></td></tr><tr><th id="L46"><a href="#L46">46</a></th><td></td></tr><tr><th id="L47"><a href="#L47">47</a></th><td>phase_image <span class="o">=</span> numpy<span class="o">.</span>angle<span class="p">(</span>src_image<span class="p">)</span></td></tr><tr><th id="L48"><a href="#L48">48</a></th><td>gdalnumeric<span class="o">.</span>SaveArray<span class="p">(</span> phase_image<span class="p">,</span> <span class="s">'phase.tif'</span> <span class="p">)</span></td></tr><tr><th id="L49"><a href="#L49">49</a></th><td></td></tr><tr><th id="L50"><a href="#L50">50</a></th><td></td></tr></tbody></table>
      </div>
      <div id="help">
        <strong>Note:</strong> See <a href="/gdal/wiki/TracBrowser">TracBrowser</a>
        for help on using the browser.
      </div>
      <div id="anydiff">
        <form action="/gdal/diff" method="get">
          <div class="buttons">
            <input type="hidden" name="new_path" value="/trunk/gdal/swig/python/samples/magphase.py" />
            <input type="hidden" name="old_path" value="/trunk/gdal/swig/python/samples/magphase.py" />
            <input type="hidden" name="new_rev" />
            <input type="hidden" name="old_rev" />
            <input type="submit" value="View changes..." title="Select paths and revs for Diff" />
          </div>
        </form>
      </div>
    </div>
    <div id="altlinks">
      <h3>Download in other formats:</h3>
      <ul>
        <li class="first">
          <a rel="nofollow" href="/gdal/browser/trunk/gdal/swig/python/samples/magphase.py?format=txt">Plain Text</a>
        </li><li class="last">
          <a rel="nofollow" href="/gdal/export/25415/trunk/gdal/swig/python/samples/magphase.py">Original Format</a>
        </li>
      </ul>
    </div>
    </div>
    <div id="footer" lang="en" xml:lang="en"><hr />
      <a id="tracpowered" href="http://trac.edgewall.org/"><img src="/gdal/chrome/common/trac_logo_mini.png" height="30" width="107" alt="Trac Powered" /></a>
      <p class="left">
        Powered by <a href="/gdal/about"><strong>Trac 0.11.7</strong></a><br />
        By <a href="http://www.edgewall.org/">Edgewall Software</a>.
      </p>
      <p class="right">Visit the Trac open source project at<br /><a href="http://trac.edgewall.org/">http://trac.edgewall.org/</a></p>
    </div>
  </body>
</html>