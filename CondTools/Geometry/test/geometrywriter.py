import FWCore.ParameterSet.Config as cms

process = cms.Process("GeometryWriter")
process.load('CondCore.CondDB.CondDB_cfi')
process.load('Configuration.Geometry.GeometryExtended_cff')
process.load('Geometry.CaloEventSetup.CaloGeometryDBWriter_cfi')
process.load('Geometry.MuonNumbering.muonNumberingInitialization_cfi')

process.source = cms.Source("EmptyIOVSource",
                            lastValue = cms.uint64(1),
                            timetype = cms.string('runnumber'),
                            firstValue = cms.uint64(1),
                            interval = cms.uint64(1)
                            )
#this and the outputservice below are set up to do the first insert of GeometryFile
process.XMLGeometryWriter = cms.EDAnalyzer("XMLGeometryBuilder",
                                           XMLFileName = cms.untracked.string("./geTagXX.xml"),
                                           ZIP = cms.untracked.bool(True)
                                           )

process.TrackerGeometricDetESModule = cms.ESProducer( "TrackerGeometricDetESModule",
                                                      fromDDD = cms.bool( True )
                                                     )


process.TrackerGeometryWriter = cms.EDAnalyzer("PGeometricDetBuilder",fromDD4hep=cms.bool( False ))
process.TrackerParametersWriter = cms.EDAnalyzer("PTrackerParametersDBBuilder", fromDD4hep=cms.bool( False ))

process.CaloGeometryWriter = cms.EDAnalyzer("PCaloGeometryBuilder")

process.CSCGeometryWriter = cms.EDAnalyzer("CSCRecoIdealDBLoader")

process.DTGeometryWriter = cms.EDAnalyzer("DTRecoIdealDBLoader")

process.RPCGeometryWriter = cms.EDAnalyzer("RPCRecoIdealDBLoader")

process.CondDB.timetype = cms.untracked.string('runnumber')
process.CondDB.connect = cms.string('sqlite_file:myfile.db')
process.PoolDBOutputService = cms.Service("PoolDBOutputService",
                                          process.CondDB,
                                          toPut = cms.VPSet(cms.PSet(record = cms.string('GeometryFileRcd'),tag = cms.string('XMLFILE_Geometry_Extended_TagXX')),
                                                            cms.PSet(record = cms.string('IdealGeometryRecord'),tag = cms.string('TKRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PTrackerParametersRcd'),tag = cms.string('TKParameters_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PEcalBarrelRcd'),   tag = cms.string('EBRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PEcalEndcapRcd'),   tag = cms.string('EERECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PEcalPreshowerRcd'),tag = cms.string('EPRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PHcalRcd'),         tag = cms.string('HCALRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PCaloTowerRcd'),    tag = cms.string('CTRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PZdcRcd'),          tag = cms.string('ZDCRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('PCastorRcd'),       tag = cms.string('CASTORRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('CSCRecoGeometryRcd'),tag = cms.string('CSCRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('CSCRecoDigiParametersRcd'),tag = cms.string('CSCRECODIGI_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('DTRecoGeometryRcd'),tag = cms.string('DTRECO_Geometry_TagXX')),
                                                            cms.PSet(record = cms.string('RPCRecoGeometryRcd'),tag = cms.string('RPCRECO_Geometry_TagXX'))
                                                            )
                                          )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
    )

process.p1 = cms.Path(process.XMLGeometryWriter+process.TrackerGeometryWriter+process.TrackerParametersWriter+process.CaloGeometryWriter+process.CSCGeometryWriter+process.DTGeometryWriter+process.RPCGeometryWriter)

